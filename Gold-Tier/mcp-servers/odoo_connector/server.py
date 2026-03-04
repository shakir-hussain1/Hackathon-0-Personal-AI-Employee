"""
Gold-Tier Odoo MCP Server
Connects to self-hosted Odoo Community via JSON-RPC.
Exposes accounting tools: invoices, partners, transactions, reports.

Odoo JSON-RPC endpoint: http://localhost:8069/jsonrpc
Authentication: /web/session/authenticate (session cookie)
External API:   /web/dataset/call_kw

Setup: see Gold-Tier/docker/docker-compose.odoo.yml
Docs:  https://www.odoo.com/documentation/19.0/developer/reference/external_api.html
"""

import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

_GOLD_ROOT = Path(__file__).parent.parent.parent
load_dotenv(_GOLD_ROOT / '.env')
sys.path.insert(0, str(_GOLD_ROOT))
from orchestrator.audit_logger import audit_log
from orchestrator.error_handler import with_retry, odoo_breaker, TransientError

ODOO_URL = os.getenv('ODOO_URL', 'http://localhost:8069')
ODOO_DB = os.getenv('ODOO_DB', 'odoo')
ODOO_USER = os.getenv('ODOO_USER', 'admin')
ODOO_PASSWORD = os.getenv('ODOO_PASSWORD', 'admin')
DRY_RUN = os.getenv('DRY_RUN', 'true').lower() == 'true'

VAULT_PATH = Path(os.getenv('VAULT_PATH', str(_GOLD_ROOT.parent / 'Common' / 'AI_Employee_Vault')))

server = Server("odoo-connector")


class OdooClient:
    """Lightweight Odoo JSON-RPC client."""

    def __init__(self):
        self.url = ODOO_URL
        self.db = ODOO_DB
        self.uid = None
        self.session = requests.Session()
        self._req_id = 0

    def _call(self, endpoint: str, method: str, params: dict) -> dict:
        self._req_id += 1
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "id": self._req_id,
            "params": params,
        }
        try:
            resp = self.session.post(
                f"{self.url}{endpoint}",
                json=payload,
                timeout=15,
            )
            resp.raise_for_status()
            result = resp.json()
            if 'error' in result:
                raise TransientError(f"Odoo error: {result['error']}")
            return result.get('result')
        except requests.exceptions.ConnectionError:
            raise TransientError(f"Cannot connect to Odoo at {self.url} — is Docker running?")
        except requests.exceptions.Timeout:
            raise TransientError("Odoo request timed out")

    @with_retry(max_attempts=3, base_delay=2)
    def authenticate(self) -> int:
        """Authenticate and return UID."""
        result = self._call('/web/session/authenticate', 'call', {
            "db": self.db,
            "login": self.user if hasattr(self, 'user') else ODOO_USER,
            "password": ODOO_PASSWORD,
        })
        if not result or not result.get('uid'):
            raise TransientError("Odoo authentication failed — check ODOO_USER/ODOO_PASSWORD in .env")
        self.uid = result['uid']
        return self.uid

    @odoo_breaker
    def execute(self, model: str, method: str, args: list = None, kwargs: dict = None):
        """Call Odoo model method via JSON-RPC."""
        if not self.uid:
            self.authenticate()
        return self._call('/web/dataset/call_kw', 'call', {
            "model": model,
            "method": method,
            "args": args or [],
            "kwargs": kwargs or {},
        })

    def search_read(self, model: str, domain: list, fields: list, limit: int = 50) -> list:
        return self.execute(model, 'search_read', [domain], {
            "fields": fields,
            "limit": limit,
        }) or []

    def create(self, model: str, values: dict) -> int:
        return self.execute(model, 'create', [values])

    def write(self, model: str, record_ids: list, values: dict) -> bool:
        return self.execute(model, 'write', [record_ids, values])


_odoo = None


def get_odoo() -> OdooClient:
    global _odoo
    if _odoo is None:
        _odoo = OdooClient()
    return _odoo


def _odoo_available() -> bool:
    try:
        get_odoo().authenticate()
        return True
    except Exception:
        return False


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="odoo_get_invoices",
            description="Get recent invoices from Odoo accounting. Returns list of invoice records.",
            inputSchema={
                "type": "object",
                "properties": {
                    "state": {
                        "type": "string",
                        "enum": ["draft", "posted", "cancel", "all"],
                        "description": "Invoice state filter (default: posted)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max records to return (default: 20)",
                    },
                },
            },
        ),
        types.Tool(
            name="odoo_create_invoice",
            description="Create a draft customer invoice in Odoo. Requires human approval before posting.",
            inputSchema={
                "type": "object",
                "required": ["partner_name", "amount", "description"],
                "properties": {
                    "partner_name": {"type": "string", "description": "Client name"},
                    "amount": {"type": "number", "description": "Invoice amount"},
                    "description": {"type": "string", "description": "Line item description"},
                    "currency": {"type": "string", "description": "Currency code (default: PKR)"},
                    "due_date_days": {"type": "integer", "description": "Days until due (default: 30)"},
                },
            },
        ),
        types.Tool(
            name="odoo_get_accounting_summary",
            description="Get accounting summary: total invoiced, paid, overdue for a period.",
            inputSchema={
                "type": "object",
                "properties": {
                    "period_days": {
                        "type": "integer",
                        "description": "Look-back period in days (default: 30)",
                    },
                },
            },
        ),
        types.Tool(
            name="odoo_get_partners",
            description="Search Odoo contacts/clients by name.",
            inputSchema={
                "type": "object",
                "properties": {
                    "search": {"type": "string", "description": "Name search string"},
                    "limit": {"type": "integer", "description": "Max results (default: 10)"},
                },
            },
        ),
        types.Tool(
            name="odoo_create_partner",
            description="Create a new contact/client in Odoo.",
            inputSchema={
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "is_company": {"type": "boolean"},
                },
            },
        ),
        types.Tool(
            name="odoo_log_transaction",
            description="Log a business transaction to the vault Accounting/ folder for the weekly audit.",
            inputSchema={
                "type": "object",
                "required": ["description", "amount", "type"],
                "properties": {
                    "description": {"type": "string"},
                    "amount": {"type": "number"},
                    "type": {"type": "string", "enum": ["income", "expense", "payment"]},
                    "client": {"type": "string"},
                    "reference": {"type": "string"},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    audit_log(f'odoo_{name}', actor='odoo-connector', target='odoo', parameters=arguments)

    if name == "odoo_get_invoices":
        return await _get_invoices(arguments)
    elif name == "odoo_create_invoice":
        return await _create_invoice(arguments)
    elif name == "odoo_get_accounting_summary":
        return await _get_accounting_summary(arguments)
    elif name == "odoo_get_partners":
        return await _get_partners(arguments)
    elif name == "odoo_create_partner":
        return await _create_partner(arguments)
    elif name == "odoo_log_transaction":
        return await _log_transaction(arguments)
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def _get_invoices(args: dict) -> list[types.TextContent]:
    state = args.get('state', 'posted')
    limit = args.get('limit', 20)

    if not _odoo_available():
        return [types.TextContent(type="text", text=
            "Odoo not available. Start with: `docker-compose -f Gold-Tier/docker/docker-compose.odoo.yml up -d`")]

    domain = [] if state == 'all' else [['move_type', '=', 'out_invoice']]
    if state not in ('all', ''):
        domain.append(['state', '=', state])

    try:
        invoices = get_odoo().search_read(
            'account.move', domain,
            ['name', 'partner_id', 'amount_total', 'state', 'invoice_date', 'invoice_date_due'],
            limit=limit,
        )
        if not invoices:
            return [types.TextContent(type="text", text="No invoices found.")]

        lines = [f"**Odoo Invoices** ({len(invoices)} records)\n"]
        total = 0
        for inv in invoices:
            partner = inv['partner_id'][1] if inv.get('partner_id') else 'N/A'
            amt = inv.get('amount_total', 0)
            total += amt
            lines.append(
                f"- {inv.get('name', 'DRAFT')} | {partner} | "
                f"{amt:,.2f} | {inv.get('state')} | Due: {inv.get('invoice_date_due', 'N/A')}"
            )
        lines.append(f"\n**Total:** {total:,.2f}")
        return [types.TextContent(type="text", text='\n'.join(lines))]
    except Exception as e:
        audit_log('odoo_get_invoices', result='error', error=str(e))
        return [types.TextContent(type="text", text=f"Odoo error: {e}")]


async def _create_invoice(args: dict) -> list[types.TextContent]:
    if DRY_RUN:
        msg = (
            f"[DRY RUN] Would create invoice:\n"
            f"  Client: {args.get('partner_name')}\n"
            f"  Amount: {args.get('amount')}\n"
            f"  Description: {args.get('description')}\n"
            "Set DRY_RUN=false in .env to create real invoices."
        )
        audit_log('odoo_create_invoice', result='dry_run', parameters=args)
        return [types.TextContent(type="text", text=msg)]

    if not _odoo_available():
        return [types.TextContent(type="text", text="Odoo not available.")]

    # Create approval file in Pending_Approval/
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    approval_file = VAULT_PATH / 'Pending_Approval' / f'INVOICE_{ts}.md'
    approval_content = f"""# Approval Required: Create Invoice
Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Action: create_odoo_invoice
Status: PENDING

## Invoice Details
- **Client:** {args.get('partner_name')}
- **Amount:** {args.get('amount')}
- **Description:** {args.get('description')}
- **Currency:** {args.get('currency', 'PKR')}
- **Due Days:** {args.get('due_date_days', 30)}

## To Approve
Move this file to `Approved/` folder.

## To Reject
Move this file to `Rejected/` folder.
"""
    approval_file.write_text(approval_content, encoding='utf-8')
    audit_log('odoo_create_invoice', approval_status='pending_human', parameters=args)
    return [types.TextContent(type="text", text=
        f"Invoice queued for approval. Review: `Pending_Approval/{approval_file.name}`")]


async def _get_accounting_summary(args: dict) -> list[types.TextContent]:
    days = args.get('period_days', 30)
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')

    # Read from vault Accounting/ logs (always available, no Odoo needed)
    accounting_dir = VAULT_PATH / 'Accounting'
    transactions = []
    for f in accounting_dir.glob('transactions_*.json'):
        try:
            for line in f.read_text(encoding='utf-8').strip().split('\n'):
                if line.strip():
                    rec = json.loads(line)
                    if rec.get('date', '') >= since:
                        transactions.append(rec)
        except Exception:
            pass

    income = sum(t['amount'] for t in transactions if t.get('type') == 'income')
    expenses = sum(t['amount'] for t in transactions if t.get('type') == 'expense')
    payments = sum(t['amount'] for t in transactions if t.get('type') == 'payment')

    summary = (
        f"**Accounting Summary — Last {days} days (since {since})**\n\n"
        f"| Category | Amount |\n|----------|--------|\n"
        f"| Income   | {income:,.2f} |\n"
        f"| Expenses | {expenses:,.2f} |\n"
        f"| Payments | {payments:,.2f} |\n"
        f"| **Net**  | **{income - expenses:,.2f}** |\n\n"
        f"Total transactions: {len(transactions)}\n"
    )

    if _odoo_available():
        summary += "\n_Live Odoo data available — run `odoo_get_invoices` for detailed records._"
    else:
        summary += "\n_Odoo offline — showing vault transaction log only. Start Odoo for full data._"

    return [types.TextContent(type="text", text=summary)]


async def _get_partners(args: dict) -> list[types.TextContent]:
    search = args.get('search', '')
    limit = args.get('limit', 10)

    if not _odoo_available():
        return [types.TextContent(type="text", text="Odoo not available.")]

    domain = [['name', 'ilike', search]] if search else []
    try:
        partners = get_odoo().search_read(
            'res.partner', domain,
            ['name', 'email', 'phone', 'is_company'],
            limit=limit,
        )
        if not partners:
            return [types.TextContent(type="text", text="No partners found.")]
        lines = [f"**Partners** ({len(partners)} found)\n"]
        for p in partners:
            kind = 'Company' if p.get('is_company') else 'Contact'
            lines.append(f"- [{kind}] {p['name']} | {p.get('email', 'N/A')} | {p.get('phone', 'N/A')}")
        return [types.TextContent(type="text", text='\n'.join(lines))]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def _create_partner(args: dict) -> list[types.TextContent]:
    if DRY_RUN:
        return [types.TextContent(type="text", text=f"[DRY RUN] Would create partner: {args}")]
    if not _odoo_available():
        return [types.TextContent(type="text", text="Odoo not available.")]
    try:
        partner_id = get_odoo().create('res.partner', {
            'name': args['name'],
            'email': args.get('email', ''),
            'phone': args.get('phone', ''),
            'is_company': args.get('is_company', True),
        })
        audit_log('odoo_create_partner', target=args['name'], result='success')
        return [types.TextContent(type="text", text=f"Partner created: {args['name']} (ID: {partner_id})")]
    except Exception as e:
        audit_log('odoo_create_partner', result='error', error=str(e))
        return [types.TextContent(type="text", text=f"Error creating partner: {e}")]


async def _log_transaction(args: dict) -> list[types.TextContent]:
    """Log transaction to Accounting/ vault folder (always works, no Odoo needed)."""
    accounting_dir = VAULT_PATH / 'Accounting'
    accounting_dir.mkdir(exist_ok=True)

    month = datetime.now().strftime('%Y-%m')
    log_file = accounting_dir / f'transactions_{month}.json'

    record = {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "timestamp": datetime.now().isoformat(),
        "description": args['description'],
        "amount": args['amount'],
        "type": args['type'],
        "client": args.get('client', ''),
        "reference": args.get('reference', ''),
    }

    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record) + '\n')

    audit_log('log_transaction', target=args.get('client', ''), parameters=record)
    return [types.TextContent(type="text", text=
        f"Transaction logged: {args['type'].upper()} {args['amount']:,.2f} — {args['description']}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == '__main__':
    asyncio.run(main())

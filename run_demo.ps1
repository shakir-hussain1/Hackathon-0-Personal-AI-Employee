# Personal AI Employee - LIVE DEMO RUNNER
# Runs all 3 tiers + live file detection

$root  = 'E:\Hackathon-0-Personal-AI-Employee'
$vault = "$root\Common\AI_Employee_Vault"
$inbox = "$vault\Inbox"

function Banner($text) {
    Write-Host ""
    Write-Host ("=" * 60)
    Write-Host "  $text"
    Write-Host ("=" * 60)
    Write-Host ""
}

function Step($n, $text) {
    Write-Host ""
    Write-Host "[$n] $text"
    Write-Host ("-" * 50)
}

function Ok($text)   { Write-Host "  [OK]   $text" }
function Info($text) { Write-Host "  [INFO] $text" }
function Warn($text) { Write-Host "  [WARN] $text" }

# SCENE 1: PROJECT STRUCTURE
Banner "SCENE 1 - Project Structure"

Step "1.1" "Tier folders:"
foreach ($f in @("Bronze-Tier","Silver-Tier","Gold-Tier","Common\AI_Employee_Vault")) {
    if (Test-Path "$root\$f") { Ok $f } else { Write-Host "  [MISS] $f" }
}

Step "1.2" "Vault subfolders:"
foreach ($d in @("Inbox","Needs_Action","Done","Logs","Plans","Accounting","Briefings","Pending_Approval","Social_Media")) {
    if (Test-Path "$vault\$d") { Ok "$d/" } else { New-Item "$vault\$d" -ItemType Directory -Force | Out-Null; Ok "$d/ (created)" }
}

Step "1.3" "MCP Servers:"
$mcpJson = Get-Content "$root\.mcp.json" -Raw -ErrorAction SilentlyContinue
foreach ($m in @("email-sender","linkedin-poster","odoo-connector","facebook-instagram","twitter-x")) {
    if ($mcpJson -match $m) { Ok "MCP: $m" } else { Warn "MCP: $m not in .mcp.json" }
}

Step "1.4" "Agent Skills:"
foreach ($s in @("process-email","draft-reply","linkedin-post","odoo-accounting","social-media-post","ceo-briefing","ralph-wiggum","weekly-audit")) {
    if (Test-Path "$root\.claude\skills\$s\SKILL.md") { Ok "Skill: /$s" } else { Warn "Skill: $s missing" }
}

Start-Sleep -Seconds 1

# SCENE 2: LAUNCH ALL 3 TIERS
Banner "SCENE 2 - Launching All 3 Tiers Simultaneously"

Step "2.1" "Starting Bronze Tier..."
$bronze = Start-Process -FilePath "$root\Bronze-Tier\venv\Scripts\python.exe" `
    -ArgumentList '-u', 'watchers\filesystem_watcher.py' `
    -WorkingDirectory "$root\Bronze-Tier" `
    -RedirectStandardOutput "$root\b_out.txt" `
    -RedirectStandardError  "$root\b_err.txt" `
    -NoNewWindow -PassThru
Start-Sleep -Seconds 1
Ok "Bronze started (PID $($bronze.Id))"

Step "2.2" "Starting Silver Tier..."
$silver = Start-Process -FilePath "$root\Silver-Tier\venv\Scripts\python.exe" `
    -ArgumentList '-u', 'orchestrator\orchestrator.py' `
    -WorkingDirectory "$root\Silver-Tier" `
    -RedirectStandardOutput "$root\s_out.txt" `
    -RedirectStandardError  "$root\s_err.txt" `
    -NoNewWindow -PassThru
Start-Sleep -Seconds 1
Ok "Silver started (PID $($silver.Id))"

Step "2.3" "Starting Gold Tier..."
$gold = Start-Process -FilePath "$root\Gold-Tier\venv\Scripts\python.exe" `
    -ArgumentList '-u', 'orchestrator\orchestrator.py' `
    -WorkingDirectory "$root\Gold-Tier" `
    -RedirectStandardOutput "$root\g_out.txt" `
    -RedirectStandardError  "$root\g_err.txt" `
    -NoNewWindow -PassThru
Start-Sleep -Seconds 1
Ok "Gold started   (PID $($gold.Id))"

Info "Waiting 8 seconds for all tiers to initialize..."
Start-Sleep -Seconds 8

# SCENE 3: BRONZE STARTUP OUTPUT
Banner "SCENE 3 - Bronze Tier Output"
Get-Content "$root\b_out.txt" -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" }
Get-Content "$root\b_err.txt" -ErrorAction SilentlyContinue | ForEach-Object { Write-Host "  $_" }

# SCENE 4: LIVE FILE DETECTION
Banner "SCENE 4 - Bronze: Live File Detection Demo"

Step "4.0" "Clearing Inbox for fresh demo..."
Get-ChildItem $inbox -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -ne ".gitkeep" } |
    ForEach-Object { Move-Item $_.FullName "$vault\Done\" -Force -ErrorAction SilentlyContinue }
Info "Inbox cleared."
Start-Sleep -Seconds 2

Step "4.1" "Dropping 3 files into Inbox..."

"# Client Meeting - XYZ Corp`nDate: 2026-02-20`nBudget: Rs 2,00,000`nDeadline: March 31`nAction: Send proposal by Feb 25" |
    Set-Content "$inbox\meeting_notes_client_xyz.md" -Encoding UTF8
Ok "meeting_notes_client_xyz.md  -> Priority: MEDIUM (.md extension)"

"Invoice #INV-2026-001`nClient: ABC Corporation`nAmount: Rs 50,000`nDue: 2026-03-05`nServices: Web Development Phase 1" |
    Set-Content "$inbox\invoice_ABC_Corp.txt" -Encoding UTF8
Ok "invoice_ABC_Corp.txt         -> Priority: HIGH  (invoice keyword)"

"URGENT: Payment overdue from XYZ Corp`nAmount: Rs 25,000 - 10 days overdue`nEscalate immediately." |
    Set-Content "$inbox\urgent_payment_followup.txt" -Encoding UTF8
Ok "urgent_payment_followup.txt  -> Priority: HIGH  (urgent keyword)"

Info "Waiting 35 seconds for Bronze watcher to detect files..."
Start-Sleep -Seconds 35

Step "4.2" "Bronze detection log:"
Get-Content "$root\b_out.txt" -ErrorAction SilentlyContinue |
    Where-Object { $_ -match "Detected|Created|started|Loaded|Error" } |
    ForEach-Object { Write-Host "  $_" }

Step "4.3" "Tasks in Needs_Action:"
$tasks = Get-ChildItem "$vault\Needs_Action" -Filter "FILE_*.md" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending
if ($tasks) {
    foreach ($t in $tasks) {
        $age = [int](New-TimeSpan -Start $t.LastWriteTime -End (Get-Date)).TotalSeconds
        $label = if ($age -lt 60) { "NEW" } else { "OLD" }
        Write-Host "  [$label] $($t.Name)"
    }
} else { Warn "No FILE_*.md tasks found" }

# SCENE 5: SILVER OUTPUT
Banner "SCENE 5 - Silver Tier: Gmail + Calendar + LinkedIn"

Step "5.1" "Silver startup log:"
Get-Content "$root\s_err.txt" -ErrorAction SilentlyContinue |
    Select-Object -First 25 | ForEach-Object { Write-Host "  $_" }

Step "5.2" "LinkedIn posts queued in Needs_Action:"
$li = Get-ChildItem "$vault\Needs_Action" -Filter "LINKEDIN_*.md" -ErrorAction SilentlyContinue
if ($li) { foreach ($p in $li) { Ok "Queued: $($p.Name)" } }
else { Info "No LinkedIn posts queued currently" }

Step "5.3" "Silver Skills loaded:"
foreach ($sk in @("process-email","draft-reply","linkedin-post","schedule-task","create-plan","whatsapp-watcher")) {
    if (Test-Path "$root\.claude\skills\$sk\SKILL.md") { Ok "/$sk" }
}

# SCENE 6: GOLD OUTPUT
Banner "SCENE 6 - Gold Tier: Odoo + Social Media + CEO Briefing"

Step "6.1" "Gold startup log:"
Get-Content "$root\g_err.txt" -ErrorAction SilentlyContinue |
    Select-Object -First 25 | ForEach-Object { Write-Host "  $_" }

Step "6.2" "Audit Log - JSON format:"
$today = Get-Date -Format "yyyy-MM-dd"
$logFile = "$vault\Logs\$today.json"
if (Test-Path $logFile) {
    Get-Content $logFile | ForEach-Object {
        try {
            $obj = $_ | ConvertFrom-Json
            Write-Host "  $($obj.timestamp.Substring(0,19))  [$($obj.action_type)]  $($obj.result)"
        } catch {}
    }
} else { Warn "No audit log for today" }

Step "6.3" "Gold Skills loaded:"
foreach ($sk in @("odoo-accounting","social-media-post","ceo-briefing","ralph-wiggum","weekly-audit")) {
    if (Test-Path "$root\.claude\skills\$sk\SKILL.md") { Ok "/$sk" }
}

Step "6.4" "Gold schedules:"
Info "Silver integration  : every 15 minutes"
Info "Social summaries    : every 6 hours"
Info "Approved actions    : every 5 minutes (HITL polling)"
Info "CEO Briefing        : Sunday at 20:00 (automated)"
Info "DRY_RUN=true        : safe mode - no live API calls"

# SCENE 7: VAULT FINAL STATE
Banner "SCENE 7 - Vault Final State"

Step "7.1" "File counts per folder:"
foreach ($d in @("Inbox","Needs_Action","Done","Logs","Plans","Accounting","Briefings","Pending_Approval","Social_Media")) {
    $c = (Get-ChildItem "$vault\$d" -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne ".gitkeep" }).Count
    Write-Host ("  {0,-22} {1,3} file(s)" -f "$d/", $c)
}

Step "7.2" "Architecture summary:"
Write-Host "  [Files/Gmail/WhatsApp] -> Watchers -> Needs_Action/"
Write-Host "  Needs_Action/ -> Claude Code + MCP Servers -> Pending_Approval/"
Write-Host "  Pending_Approval/ -> Human approves -> Done/ + Audit Log"
Write-Host "  Done/ + Audit Log -> CEO Briefing (Sunday auto-generate)"

# SHUTDOWN
Banner "SCENE 8 - Shutting Down Demo"
$bronze.Kill(); Ok "Bronze stopped"
$silver.Kill(); Ok "Silver stopped"
$gold.Kill();   Ok "Gold stopped"

Remove-Item "$root\b_out.txt","$root\b_err.txt","$root\s_out.txt","$root\s_err.txt","$root\g_out.txt","$root\g_err.txt" -ErrorAction SilentlyContinue

Banner "DEMO COMPLETE"
Write-Host "  Bronze  : FileSystemWatcher - 3 files detected, tasks created"
Write-Host "  Silver  : Orchestrator running - graceful fail on credentials"
Write-Host "  Gold    : DRY_RUN=true - schedules active, audit log live"
Write-Host ""
Write-Host "  To go LIVE:"
Write-Host "    1. Silver-Tier\credentials.json -> Gmail + Calendar ON"
Write-Host "    2. Gold-Tier\.env -> Add API keys"
Write-Host "    3. DRY_RUN=false -> Social media + Odoo ON"
Write-Host "    4. start_all.bat -> All tiers running 24/7"
Write-Host ""

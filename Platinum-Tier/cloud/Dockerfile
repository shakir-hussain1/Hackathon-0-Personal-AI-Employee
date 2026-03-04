FROM python:3.13-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copy cloud agent files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Security: secrets must be mounted at runtime, never baked into image
# Mount: -v /host/secrets/.env:/app/.env:ro
# Mount: -v /host/secrets/credentials.json:/secrets/credentials.json:ro

ENV PYTHONUNBUFFERED=1
ENV DRY_RUN=true
ENV ENABLE_GMAIL=false

CMD ["python", "cloud_orchestrator.py"]

#!/usr/bin/env bash
# One-shot setup: creates n8n credentials + deploys CRM sync workflow
# Run from any machine with network access to whenmoney.app.n8n.cloud
#
# Usage:
#   N8N_API_KEY=<your-key> ANTHROPIC_API_KEY=<key> ATTIO_API_KEY=<bearer-token> bash tools/n8n-mcp/setup.sh
#
# Or export vars first:
#   export N8N_API_KEY=...
#   export ANTHROPIC_API_KEY=...
#   export ATTIO_API_KEY=...   (just the token, without "Bearer ")
#   bash tools/n8n-mcp/setup.sh

set -e

N8N_BASE="${N8N_BASE_URL:-https://whenmoney.app.n8n.cloud}"
API="$N8N_BASE/api/v1"
KEY="${N8N_API_KEY:?N8N_API_KEY must be set}"
ANTHROPIC_KEY="${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY must be set}"
ATTIO_TOKEN="${ATTIO_API_KEY:?ATTIO_API_KEY must be set}"

WORKFLOW_JSON="$(cd "$(dirname "$0")/../.." && pwd)/workflows/n8n/crm-sync-from-transcripts-v3.json"

echo "→ n8n instance: $N8N_BASE"
echo ""

# ── 1. Check / create Anthropic credential ──────────────────────────────────
echo "[1/4] Creating Anthropic API credential..."
ANTHROPIC_DATA=$(python3 -c "import json,sys; print(json.dumps(json.dumps({'name':'x-api-key','value':sys.argv[1],'allowedDomains':[]}))" "$ANTHROPIC_KEY")
ANTHROPIC_CRED=$(curl -sf -X POST "$API/credentials" \
  -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Anthropic API\",\"type\":\"httpHeaderAuth\",\"data\":$ANTHROPIC_DATA}")
ANTHROPIC_ID=$(echo "$ANTHROPIC_CRED" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "   ✓ Anthropic credential ID: $ANTHROPIC_ID"

# ── 2. Create Attio credential ───────────────────────────────────────────────
echo "[2/4] Creating Attio API credential..."
ATTIO_DATA=$(python3 -c "import json,sys; print(json.dumps(json.dumps({'name':'Authorization','value':'Bearer '+sys.argv[1],'allowedDomains':[]}))" "$ATTIO_TOKEN")
ATTIO_CRED=$(curl -sf -X POST "$API/credentials" \
  -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Attio API\",\"type\":\"httpHeaderAuth\",\"data\":$ATTIO_DATA}")
ATTIO_ID=$(echo "$ATTIO_CRED" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "   ✓ Attio credential ID: $ATTIO_ID"

# ── 3. Patch workflow JSON with real credential IDs ──────────────────────────
echo "[3/4] Patching workflow JSON with credential IDs..."
PATCHED=$(python3 - "$WORKFLOW_JSON" "$ANTHROPIC_ID" "$ATTIO_ID" <<'PYEOF'
import sys, json

path, ant_id, att_id = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    wf = json.load(f)

for node in wf.get("nodes", []):
    creds = node.get("credentials", {})
    if "httpHeaderAuth" in creds:
        name = creds["httpHeaderAuth"].get("name", "")
        if name == "Anthropic API":
            creds["httpHeaderAuth"]["id"] = ant_id
        elif name == "Attio API":
            creds["httpHeaderAuth"]["id"] = att_id

print(json.dumps(wf))
PYEOF
)
echo "   ✓ Credential IDs patched"

# ── 4. Deploy workflow ───────────────────────────────────────────────────────
echo "[4/4] Deploying workflow to n8n..."
DEPLOY=$(echo "$PATCHED" | curl -sf -X POST "$API/workflows" \
  -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" \
  -d @-)
WF_ID=$(echo "$DEPLOY" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "   ✓ Workflow deployed — ID: $WF_ID"

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setup complete!"
echo "  Anthropic credential: $ANTHROPIC_ID"
echo "  Attio credential:     $ATTIO_ID"
echo "  Workflow ID:          $WF_ID"
echo ""
echo "Test run:"
echo "  curl -X POST \"$API/workflows/$WF_ID/run\" -H \"X-N8N-API-KEY: \$N8N_API_KEY\" -H \"Content-Type: application/json\" -d '{}'"
echo ""
echo "To use from Claude Code, update .claude/settings.local.json N8N_API_KEY if needed."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

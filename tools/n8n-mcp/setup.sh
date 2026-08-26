#!/usr/bin/env bash
# Deploy CRM Sync from Transcripts v3 workflow to n8n
#
# Usage:
#   N8N_API_KEY=<key> ANTHROPIC_API_KEY=<key> ATTIO_API_KEY=<token> bash tools/n8n-mcp/setup.sh
#
# Keys are substituted in-memory before deploy — never written to disk.

set -e

N8N_BASE="${N8N_BASE_URL:-https://whenmoney.app.n8n.cloud}"
API="$N8N_BASE/api/v1"
KEY="${N8N_API_KEY:?N8N_API_KEY must be set}"
ANTHROPIC_KEY="${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY must be set}"
ATTIO_TOKEN="${ATTIO_API_KEY:?ATTIO_API_KEY must be set}"

WORKFLOW_JSON="$(cd "$(dirname "$0")/../.." && pwd)/workflows/n8n/crm-sync-from-transcripts-v3.json"

echo "→ n8n instance: $N8N_BASE"
echo ""

echo "[1/1] Deploying workflow..."

# Substitute placeholders in-memory, then POST directly to n8n
DEPLOY=$(python3 - "$WORKFLOW_JSON" "$ANTHROPIC_KEY" "$ATTIO_TOKEN" <<'PYEOF'
import sys, json

path, anthropic_key, attio_token = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path) as f:
    wf = json.load(f)

wf_str = json.dumps(wf)
wf_str = wf_str.replace("ANTHROPIC_API_KEY_PLACEHOLDER", anthropic_key)
wf_str = wf_str.replace("ATTIO_API_KEY_PLACEHOLDER", attio_token)
print(wf_str)
PYEOF
)

RESPONSE=$(echo "$DEPLOY" | curl -s -w "\n%{http_code}" -X POST "$API/workflows" \
  -H "X-N8N-API-KEY: $KEY" \
  -H "Content-Type: application/json" \
  -d @-)

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" != "200" ] && [ "$HTTP_CODE" != "201" ]; then
  echo "   ✗ Deploy failed (HTTP $HTTP_CODE)"
  echo "   $BODY"
  exit 1
fi

WF_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "   ✓ Workflow deployed — ID: $WF_ID"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Done! Workflow ID: $WF_ID"
echo "Open: $N8N_BASE/workflow/$WF_ID"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

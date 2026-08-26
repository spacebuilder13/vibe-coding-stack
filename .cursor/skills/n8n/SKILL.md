# Skill: n8n

Build, deploy, run, and debug n8n automation workflows from Claude Code using the n8n MCP server.

**Trigger phrases:** "build a workflow", "n8n", "automate", "run the workflow", "deploy workflow",
"CRM sync", "trigger workflow", "debug workflow", "what workflows do I have".

---

## What this skill does

Gives Claude Code full autonomy over the n8n instance at `whenmoney.app.n8n.cloud`:
- List and inspect existing workflows
- Create or update workflows by generating and deploying JSON
- Execute workflows manually and poll execution output
- Debug failures by reading node-level output from execution logs
- Version-control workflow JSON in `workflows/n8n/`

---

## Pre-flight: MCP server setup (one-time)

```bash
cd tools/n8n-mcp && npm install
```

Add to `.claude/settings.json` under `mcpServers`:
```json
{
  "n8n-mcp": {
    "command": "node",
    "args": ["tools/n8n-mcp/index.js"],
    "env": {
      "N8N_BASE_URL": "https://whenmoney.app.n8n.cloud",
      "N8N_API_KEY": "<your n8n API key>"
    }
  }
}
```

Get your n8n API key: n8n UI → Settings → API → Create API Key.

---

## n8n credential setup (one-time, in n8n UI)

| Credential name | Type | Config |
|----------------|------|--------|
| `Google Drive OAuth2 API` | Google Drive OAuth2 | OAuth flow in n8n |
| `Anthropic API` | HTTP Header Auth | Header: `x-api-key`, Value: `<Anthropic key>` |
| `Attio API` | HTTP Header Auth | Header: `Authorization`, Value: `Bearer <Attio token>` |

After import, re-assign credentials in each workflow node's credential selector.

---

## Standard workflow

### Deploy a new workflow from JSON
```
1. Edit or create workflows/n8n/<name>.json
2. Use create_workflow tool with the JSON content
3. n8n returns the workflow ID — note it
4. Use execute_workflow with the ID to test
5. Use get_execution with the execution ID to see output
```

### Debug a failing workflow
```
1. get_executions workflowId=<id> — find the latest failed run
2. get_execution id=<executionId> includeData=true — see exactly which node failed and why
3. Fix the workflow JSON, update_workflow
4. Re-run and verify
```

### Import pre-built workflow
```
1. Read workflows/n8n/crm-sync-from-transcripts-v3.json
2. create_workflow with the JSON
3. In n8n UI: assign credentials to the 3 HTTP nodes (Anthropic, Attio ×3)
4. Run and check executions
```

---

## Workflow registry

| File | Purpose | n8n ID |
|------|---------|--------|
| `crm-sync-from-transcripts-v3.json` | Batch sync WHEN Travel Google Drive transcripts → Attio CRM | assign after deploy |

---

## Key constants

| Item | Value |
|------|-------|
| n8n instance | `https://whenmoney.app.n8n.cloud` |
| Google Drive folder | `1W3wLJTBeXuFcBaWVNpCHnyenFIoc2gRY` |
| Attio list (WHEN Travel clients) | `4bd161bd-2b58-4c11-9ee5-004257444bb2` |
| Attio people field slugs | `name`, `name_2`, `destination_city`, `time_to_travel`, `budget_range`, `blockers_pain_point`, `jtbd`, `journey_stage`, `memorable_quotes` |
| Claude model for extraction | `claude-haiku-4-5-20251001` |

---

## Output checklist

- [ ] `tools/n8n-mcp/` installed (`npm install`)
- [ ] MCP server wired in `.claude/settings.json`
- [ ] Workflow deployed via `create_workflow`
- [ ] Credentials assigned in n8n UI
- [ ] Test execution successful (all nodes green)
- [ ] Attio record created/updated with correct fields
- [ ] Workflow JSON committed to `workflows/n8n/`

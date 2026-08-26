import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const BASE = process.env.N8N_BASE_URL?.replace(/\/$/, "");
const KEY = process.env.N8N_API_KEY;

if (!BASE || !KEY) {
  process.stderr.write("N8N_BASE_URL and N8N_API_KEY must be set\n");
  process.exit(1);
}

async function n8n(method, path, body) {
  const res = await fetch(`${BASE}/api/v1${path}`, {
    method,
    headers: { "X-N8N-API-KEY": KEY, "Content-Type": "application/json" },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`n8n ${method} ${path} → ${res.status}: ${text}`);
  return text ? JSON.parse(text) : {};
}

const TOOLS = [
  {
    name: "list_workflows",
    description: "List all workflows in the n8n instance",
    inputSchema: { type: "object", properties: {}, required: [] },
  },
  {
    name: "get_workflow",
    description: "Get the full JSON definition of a workflow by ID",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string", description: "Workflow ID" } },
      required: ["id"],
    },
  },
  {
    name: "create_workflow",
    description: "Create a new workflow from a JSON definition. Returns the created workflow with its assigned ID.",
    inputSchema: {
      type: "object",
      properties: { workflow: { type: "object", description: "Full n8n workflow JSON (nodes, connections, name, settings)" } },
      required: ["workflow"],
    },
  },
  {
    name: "update_workflow",
    description: "Replace an existing workflow's definition by ID",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string" },
        workflow: { type: "object", description: "Updated workflow JSON" },
      },
      required: ["id", "workflow"],
    },
  },
  {
    name: "activate_workflow",
    description: "Activate a workflow so its triggers fire",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string" } },
      required: ["id"],
    },
  },
  {
    name: "deactivate_workflow",
    description: "Deactivate a workflow",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string" } },
      required: ["id"],
    },
  },
  {
    name: "execute_workflow",
    description: "Manually trigger a workflow execution. Returns an executionId to track with get_execution.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "Workflow ID" },
        inputData: { type: "object", description: "Optional JSON data to pass as workflow input" },
      },
      required: ["id"],
    },
  },
  {
    name: "get_executions",
    description: "List recent executions for a workflow, newest first",
    inputSchema: {
      type: "object",
      properties: {
        workflowId: { type: "string" },
        limit: { type: "number", default: 10, description: "Max results (default 10)" },
        status: { type: "string", enum: ["success", "error", "waiting"], description: "Filter by status" },
      },
      required: ["workflowId"],
    },
  },
  {
    name: "get_execution",
    description: "Get full details and node-level output of a specific execution",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "Execution ID" },
        includeData: { type: "boolean", default: true, description: "Include node output data" },
      },
      required: ["id"],
    },
  },
  {
    name: "delete_workflow",
    description: "Permanently delete a workflow by ID",
    inputSchema: {
      type: "object",
      properties: { id: { type: "string" } },
      required: ["id"],
    },
  },
];

const server = new Server({ name: "n8n-mcp", version: "1.0.0" }, { capabilities: { tools: {} } });

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: TOOLS }));

server.setRequestHandler(CallToolRequestSchema, async (req) => {
  const { name, arguments: args } = req.params;
  try {
    let result;
    switch (name) {
      case "list_workflows":
        result = await n8n("GET", "/workflows?limit=100&active=false");
        break;
      case "get_workflow":
        result = await n8n("GET", `/workflows/${args.id}`);
        break;
      case "create_workflow":
        result = await n8n("POST", "/workflows", args.workflow);
        break;
      case "update_workflow":
        result = await n8n("PUT", `/workflows/${args.id}`, args.workflow);
        break;
      case "activate_workflow":
        result = await n8n("POST", `/workflows/${args.id}/activate`);
        break;
      case "deactivate_workflow":
        result = await n8n("POST", `/workflows/${args.id}/deactivate`);
        break;
      case "execute_workflow":
        result = await n8n("POST", `/workflows/${args.id}/run`, { data: args.inputData ?? {} });
        break;
      case "get_executions": {
        const qs = `workflowId=${args.workflowId}&limit=${args.limit ?? 10}${args.status ? `&status=${args.status}` : ""}`;
        result = await n8n("GET", `/executions?${qs}`);
        break;
      }
      case "get_execution":
        result = await n8n("GET", `/executions/${args.id}?includeData=${args.includeData !== false}`);
        break;
      case "delete_workflow":
        result = await n8n("DELETE", `/workflows/${args.id}`);
        break;
      default:
        throw new Error(`Unknown tool: ${name}`);
    }
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  } catch (err) {
    return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);

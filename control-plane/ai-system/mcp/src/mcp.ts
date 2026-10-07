import { createMcpHandler, McpServer } from "@modelcontextprotocol/server";
import * as z from "zod/v4";

import { readCapabilities, runBridge, submitEnabled } from "./bridge.js";
import { memoryWriteEnabled, runMemory } from "./memory.js";

export const GATEWAY_VERSION = "0.1.0";

function toolResult(payload: Record<string, unknown>) {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(payload) }],
    structuredContent: payload,
  };
}

export function createGatewayServer(): McpServer {
  const server = new McpServer({
    name: "ordinary-chat-agent-gateway",
    version: GATEWAY_VERSION,
  });

  server.registerTool(
    "capabilities",
    {
      title: "Ordinary Chat Capabilities",
      description:
        "Use this to inspect the configured ordinary-chat execution layers and their declared availability before choosing a route.",
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async () => toolResult(readCapabilities()),
  );

  server.registerTool(
    "bridge_preflight",
    {
      title: "Local Bridge Preflight",
      description:
        "Use this before local reads/writes or agent launches to verify allowlists and configured local runtimes. It does not mutate files.",
      inputSchema: z.object({ workspace: z.string().optional(), repo: z.string().optional() }),
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async ({ workspace, repo }) => {
      const args = ["preflight"];
      if (workspace) args.push("--workspace", workspace);
      if (repo) args.push("--repo", repo);
      return toolResult(runBridge(args));
    },
  );

  server.registerTool(
    "agent_run_status",
    {
      title: "Agent Run Status",
      description:
        "Use this to inspect a previously queued ordinary-chat or A01-A10 local agent run by run id.",
      inputSchema: z.object({ runId: z.string().regex(/^[0-9a-f]{32}$/) }),
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async ({ runId }) => toolResult(runBridge(["status", "--run-id", runId])),
  );

  server.registerTool(
    "agent_receipt_summary",
    {
      title: "Agent Receipt Summary",
      description:
        "Use this to retrieve a safe summary of one A01-A10 actor receipt after a run has produced receipts.",
      inputSchema: z.object({
        runId: z.string().regex(/^[0-9a-f]{32}$/),
        actor: z.enum(["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10"]),
      }),
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async ({ runId, actor }) =>
      toolResult(runBridge(["receipt-summary", "--run-id", runId, "--actor", actor])),
  );

  server.registerTool(
    "project_memory_search",
    {
      title: "Project Memory Search",
      description:
        "Use this to search explicitly saved, project-scoped local memory with provenance. It never saves conversation content automatically.",
      inputSchema: z.object({
        workspace: z.string().min(1),
        query: z.string().max(2000).default(""),
        limit: z.number().int().min(1).max(50).default(10),
      }),
      annotations: { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false },
    },
    async ({ workspace, query, limit }) =>
      toolResult(runMemory(["search", "--workspace", workspace, "--query", query, "--limit", String(limit)])),
  );

  if (submitEnabled()) {
    server.registerTool(
      "agent_submit_chat_work",
      {
        title: "Submit Local Chat Work",
        description:
          "Use this only after bridge_preflight passes to queue a long local task through the configured chat-work-agent bridge in an allowlisted workspace.",
        inputSchema: z.object({ workspace: z.string().min(1), goal: z.string().min(1).max(20000) }),
        annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false },
      },
      async ({ workspace, goal }) =>
        toolResult(runBridge(["submit-chat", "--workspace", workspace], goal)),
    );

    server.registerTool(
      "agent_submit_a01_a10",
      {
        title: "Submit Governed A01-A10 Run",
        description:
          "Use this only after preflight to queue the existing receipt-bound A01-A10 workflow. Only A07 receives the explicit write-set; all other actors remain read-only.",
        inputSchema: z.object({
          repo: z.string().min(1),
          issue: z.number().int().positive(),
          baseRef: z.string().min(1).default("main"),
          goal: z.string().min(1).max(20000),
          writeSet: z.array(z.string().min(1)).max(100).default([]),
          maxParallel: z.number().int().min(1).max(10).default(3),
          timeoutSeconds: z.number().min(10).max(3600).default(180),
          maxBudgetUsd: z.number().min(0).max(100).default(0.05),
          model: z.string().optional(),
        }),
        annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false },
      },
      async ({ repo, issue, baseRef, goal, writeSet, maxParallel, timeoutSeconds, maxBudgetUsd, model }) => {
        const args = [
          "submit-a01", "--repo", repo, "--issue", String(issue), "--base-ref", baseRef,
          "--max-parallel", String(maxParallel), "--timeout-seconds", String(timeoutSeconds),
          "--max-budget-usd", String(maxBudgetUsd),
        ];
        for (const item of writeSet) args.push("--write-set", item);
        if (model) args.push("--model", model);
        return toolResult(runBridge(args, goal));
      },
    );

    if (memoryWriteEnabled()) {
      server.registerTool(
        "project_memory_add",
        {
          title: "Project Memory Add",
          description:
            "Use this only for explicit user-approved project memory. Store content with source, confidence, retention, and tags; never use it for automatic transcript capture.",
          inputSchema: z.object({
            workspace: z.string().min(1),
            content: z.string().min(1).max(20000),
            source: z.string().min(1).max(2000),
            confidence: z.number().min(0).max(1).default(1),
            retention: z.enum(["ephemeral", "project", "durable"]).default("project"),
            tags: z.array(z.string().min(1).max(100)).max(30).default([]),
          }),
          annotations: { readOnlyHint: false, destructiveHint: false, idempotentHint: false, openWorldHint: false },
        },
        async ({ workspace, content, source, confidence, retention, tags }) => {
          const args = [
            "add", "--workspace", workspace, "--source", source,
            "--confidence", String(confidence), "--retention", retention,
          ];
          for (const tag of tags) args.push("--tag", tag);
          return toolResult(runMemory(args, content));
        },
      );

      server.registerTool(
        "project_memory_delete",
        {
          title: "Project Memory Delete",
          description: "Use this to explicitly delete one saved local project-memory item by id.",
          inputSchema: z.object({ workspace: z.string().min(1), id: z.string().regex(/^[0-9a-f]{32}$/) }),
          annotations: { readOnlyHint: false, destructiveHint: true, idempotentHint: true, openWorldHint: false },
        },
        async ({ workspace, id }) =>
          toolResult(runMemory(["delete", "--workspace", workspace, "--id", id])),
      );
    }
  }

  return server;
}

export function createGatewayHandler() {
  return createMcpHandler(() => createGatewayServer());
}

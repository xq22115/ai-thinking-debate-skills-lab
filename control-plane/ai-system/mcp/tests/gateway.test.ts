import assert from "node:assert/strict";
import test from "node:test";
import { Client, StreamableHTTPClientTransport } from "@modelcontextprotocol/client";

import { createGatewayHandler } from "../src/mcp.js";

const DEFAULT_READ_ONLY_TOOLS = [
  "agent_receipt_summary",
  "agent_run_liveness",
  "agent_run_status",
  "bridge_preflight",
  "capabilities",
  "capability_health",
  "capability_route",
  "project_memory_search",
].sort();

test("gateway exposes only the expected read-only default surface", async () => {
  process.env.ORDINARY_CHAT_MCP_ALLOW_SUBMIT = "false";
  process.env.ORDINARY_CHAT_MEMORY_ALLOW_WRITE = "false";
  delete process.env.ORDINARY_CHAT_ALLOWED_ROOTS;

  const handler = createGatewayHandler();
  const transport = new StreamableHTTPClientTransport(new URL("http://test.local/mcp"), {
    fetch: (url, init) => handler.fetch(new Request(url, init)),
  });
  const client = new Client(
    { name: "ordinary-chat-gateway-test", version: "1.0.0" },
    { versionNegotiation: { mode: "auto" } },
  );

  try {
    await client.connect(transport);
    const listed = await client.listTools();
    const names = listed.tools.map((tool) => tool.name).sort();
    assert.deepEqual(names, DEFAULT_READ_ONLY_TOOLS);
    assert.equal(names.includes("agent_submit_chat_work"), false);
    assert.equal(names.includes("agent_submit_a01_a10"), false);
    assert.equal(names.includes("project_memory_add"), false);
    assert.equal(names.includes("project_memory_delete"), false);

    for (const tool of listed.tools) {
      assert.equal(tool.annotations?.readOnlyHint, true, `${tool.name} must be read-only by default`);
      assert.equal(tool.annotations?.destructiveHint, false, `${tool.name} must not be destructive`);
    }

    const capabilities = await client.callTool({ name: "capabilities", arguments: {} });
    const capabilityData = capabilities.structuredContent as Record<string, unknown>;
    assert.equal(capabilityData.schemaVersion, 1);
    assert.ok(Array.isArray(capabilityData.capabilities));

    const health = await client.callTool({ name: "capability_health", arguments: {} });
    const healthData = health.structuredContent as Record<string, unknown>;
    assert.equal(healthData.result, "PASS");
    assert.equal(healthData.schemaVersion, 1);
    assert.equal(typeof healthData.capabilities, "object");

    const route = await client.callTool({
      name: "capability_route",
      arguments: { intent: "repository_action" },
    });
    const routeData = route.structuredContent as Record<string, unknown>;
    assert.equal(routeData.result, "CONDITIONAL");
    const selected = routeData.selected as Record<string, unknown>;
    assert.equal(selected.id, "github-native");

    const readyOnlyRoute = await client.callTool({
      name: "capability_route",
      arguments: { intent: "repository_action", requireReady: true },
    });
    const readyOnlyData = readyOnlyRoute.structuredContent as Record<string, unknown>;
    assert.equal(readyOnlyData.result, "BLOCKED");
    assert.equal(readyOnlyData.reason, "no_compatible_ready_route");

    const preflight = await client.callTool({ name: "bridge_preflight", arguments: {} });
    const preflightData = preflight.structuredContent as Record<string, unknown>;
    assert.equal(preflightData.result, "BLOCKED");
    assert.equal(preflightData.allowed_roots_configured, false);

    const liveness = await client.callTool({
      name: "agent_run_liveness",
      arguments: { runId: "f".repeat(32) },
    });
    const livenessData = liveness.structuredContent as Record<string, unknown>;
    assert.equal(livenessData.result, "NOT_FOUND");
    assert.equal(livenessData.schemaVersion, 2);
  } finally {
    await client.close();
    await handler.close();
  }
});

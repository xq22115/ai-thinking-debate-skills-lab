import { createServer } from "node:http";
import { timingSafeEqual } from "node:crypto";
import {
  hostHeaderValidation,
  localhostHostValidation,
  localhostOriginValidation,
  originValidation,
  toNodeHandler,
} from "@modelcontextprotocol/node";

import { createGatewayHandler, GATEWAY_VERSION } from "./mcp.js";
import { submitEnabled } from "./bridge.js";

function csv(name: string): string[] {
  return (process.env[name] ?? "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function isLoopback(host: string): boolean {
  return host === "127.0.0.1" || host === "localhost" || host === "::1";
}

function bearerAllowed(header: string | undefined, token: string): boolean {
  if (!token) return true;
  const prefix = "Bearer ";
  if (!header?.startsWith(prefix)) return false;
  const supplied = Buffer.from(header.slice(prefix.length));
  const expected = Buffer.from(token);
  return supplied.length === expected.length && timingSafeEqual(supplied, expected);
}

const PORT = Number(process.env.PORT ?? 3000);
const BIND_HOST = process.env.BIND_HOST?.trim() || "127.0.0.1";
const allowedHosts = csv("MCP_ALLOWED_HOSTS");
const allowedOrigins = csv("MCP_ALLOWED_ORIGINS");
const bearerToken = process.env.MCP_BEARER_TOKEN ?? "";
const allowUnauthenticatedRemote = process.env.MCP_ALLOW_UNAUTHENTICATED_REMOTE === "true";

if (!isLoopback(BIND_HOST)) {
  if (allowedHosts.length === 0) {
    throw new Error("remote_bind_requires_MCP_ALLOWED_HOSTS");
  }
  if (!bearerToken && !allowUnauthenticatedRemote) {
    throw new Error("remote_bind_requires_auth_or_explicit_override");
  }
}

const handler = createGatewayHandler();
const nodeHandler = toNodeHandler(handler);
const validateHost =
  allowedHosts.length > 0 ? hostHeaderValidation(allowedHosts) : localhostHostValidation();
const validateOrigin =
  allowedOrigins.length > 0 ? originValidation(allowedOrigins) : localhostOriginValidation();

const httpServer = createServer((req, res) => {
  const pathname = (req.url ?? "/").split("?")[0];

  if (pathname === "/healthz") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(
      JSON.stringify({
        ok: true,
        version: GATEWAY_VERSION,
        submit_enabled: submitEnabled(),
      }),
    );
    return;
  }

  if (pathname !== "/mcp") {
    res.writeHead(404, { "content-type": "application/json" });
    res.end(JSON.stringify({ error: "not_found" }));
    return;
  }

  if (!validateHost(req, res) || !validateOrigin(req, res)) return;
  if (!bearerAllowed(req.headers.authorization, bearerToken)) {
    res.writeHead(401, {
      "content-type": "application/json",
      "www-authenticate": "Bearer",
    });
    res.end(JSON.stringify({ error: "unauthorized" }));
    return;
  }

  void nodeHandler(req, res);
});

httpServer.listen(PORT, BIND_HOST, () => {
  console.log(
    `ordinary-chat-agent-gateway v${GATEWAY_VERSION} listening on http://${BIND_HOST}:${PORT}/mcp`,
  );
});

async function shutdown(signal: string) {
  console.log(`received ${signal}; shutting down`);
  httpServer.close();
  await handler.close();
  process.exit(0);
}

process.on("SIGINT", () => void shutdown("SIGINT"));
process.on("SIGTERM", () => void shutdown("SIGTERM"));

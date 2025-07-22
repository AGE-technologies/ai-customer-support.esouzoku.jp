import { Hono } from "hono";
import { handleHubSpotWebhook } from "./handlers/webhook.ts";
import { handleRagUpdate } from "./handlers/rag.ts";

export function createApp() {
  const app = new Hono();

  app.get("/", (c) => {
    return c.json({ message: "AI Customer Support API" });
  });

  app.get("/health", (c) => {
    return c.json({ status: "OK", service: "ai-customer-support" });
  });

  app.post("/webhook/hubspot", handleHubSpotWebhook);
  
  app.post("/rag/update", handleRagUpdate);

  return app;
}

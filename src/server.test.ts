import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import { createApp } from "./server.ts";

Deno.test("GET /health returns 200 with OK message", async () => {
  const app = createApp();
  const req = new Request("http://localhost/health");
  const res = await app.request(req);

  assertEquals(res.status, 200);
  assertEquals(await res.json(), {
    status: "OK",
    service: "ai-customer-support",
  });
});

Deno.test("GET / returns welcome message", async () => {
  const app = createApp();
  const req = new Request("http://localhost/");
  const res = await app.request(req);

  assertEquals(res.status, 200);
  assertEquals(await res.json(), { message: "AI Customer Support API" });
});

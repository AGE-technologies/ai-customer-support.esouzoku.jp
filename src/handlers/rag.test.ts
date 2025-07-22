import { assertEquals } from "https://deno.land/std@0.208.0/assert/mod.ts";
import { createApp } from "../server.ts";

Deno.test("POST /rag/update processes RAG data update", async () => {
  const app = createApp();
  
  const req = new Request("http://localhost/rag/update", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  const res = await app.request(req);
  
  assertEquals(res.status, 200);
  const response = await res.json();
  assertEquals(response.status, "started");
  assertEquals(typeof response.jobId, "string");
});
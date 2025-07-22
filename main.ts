import { createApp } from "./src/server.ts";

const app = createApp();
const port = Number(Deno.env.get("PORT")) || 8000;

console.log(`Server starting on port ${port}`);
Deno.serve({ port }, app.fetch);

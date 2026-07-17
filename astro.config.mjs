import { defineConfig } from "astro/config";

// Static site. No server, no DB contact at runtime.
export default defineConfig({
  output: "static",
  site: "https://beforethetoken.example",
});

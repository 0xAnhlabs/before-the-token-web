import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Static site. No server, no DB contact at runtime.
export default defineConfig({
  output: "static",
  site: "https://beforethetoken.vercel.app",
  integrations: [sitemap()],
});

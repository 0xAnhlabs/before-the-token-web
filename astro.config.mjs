import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Static site. No server, no DB contact at runtime.
export default defineConfig({
  output: "static",
  site: "https://beforethetoken.vercel.app",
  integrations: [sitemap({
    // Generate single sitemap.xml (not index) for Google compatibility
    changefreq: "weekly",
    priority: 0.7,
  })],
  trailingSlash: "always",
});

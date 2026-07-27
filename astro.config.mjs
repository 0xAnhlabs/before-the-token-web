import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import vercel from "@astrojs/vercel/static";

// Static site. No server, no DB contact at runtime.
export default defineConfig({
  output: "static",
  site: "https://beforethetoken.vercel.app",
  adapter: vercel({
    webAnalytics: { enabled: true },
  }),
  integrations: [sitemap()],
});

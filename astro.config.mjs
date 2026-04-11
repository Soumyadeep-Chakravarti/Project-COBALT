import { defineConfig } from "astro/config";
import mermaid from "astro-mermaid";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import rehypeSlug from "rehype-slug";

export default defineConfig({
  // Base URL for GitHub Pages (Repo name with leading slash)
  base: "/Project-COBALT",
  // Your GitHub Pages URL
  site: "https://Soumyadeep-Chakravarti.github.io",

  srcDir: "./docs/src",
  outDir: "./dist",
  publicDir: "./docs/public",

  image: {
    service: {
      entrypoint: "astro/assets/services/noop",
    },
  },
  markdown: {
    remarkPlugins: [remarkGfm],
    rehypePlugins: [rehypeHighlight, rehypeSlug],
  },
  integrations: [mermaid()],
  vite: {
    build: {
      chunkSizeWarningLimit: 600,
    },
  },
});


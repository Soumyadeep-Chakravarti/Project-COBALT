import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";

/**
 * Custom Remark plugin to wrap mermaid code blocks in a <pre> tag.
 */
function remarkMermaid() {
  return function (tree) {
    tree.children.forEach((node, i) => {
      if (node.type === "code" && node.lang === "mermaid") {
        const html = `<pre class="mermaid">${node.value}</pre>`;
        tree.children[i] = { type: "html", value: html };
      }
    });
  };
}

export default defineConfig({
  base: "/Project-COBALT/",

  // Updated to your GitHub Pages URL
  site: "https://soumyadeep-chakravarti.github.io",

  srcDir: "./src",
  outDir: "./dist",
  publicDir: "./public",

  image: {
    service: {
      entrypoint: "astro/assets/services/noop",
    },
  },
  markdown: {
    // Fixed: remarkMermaid should not be wrapped in double brackets if it has no options
    remarkPlugins: [remarkMermaid, remarkGfm],
    rehypePlugins: [rehypeSlug],
  },
  integrations: [sitemap()],
  vite: {
    build: {
      chunkSizeWarningLimit: 600,
    },
  },
});


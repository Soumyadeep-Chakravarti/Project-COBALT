import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";
import rehypePrettyCode from "rehype-pretty-code";

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

  site: "https://soumyadeep-chakravarti.github.io/Project-COBALT",

  srcDir: "./src",
  outDir: "./dist",
  publicDir: "./public",

  image: {
    service: {
      entrypoint: "astro/assets/services/noop",
    },
  },
  markdown: {
    remarkPlugins: [remarkMermaid, remarkGfm],
    rehypePlugins: [
      rehypeSlug,
      [rehypePrettyCode, { theme: { dark: "github-dark", light: "github-light" }, keepBackground: false }]
    ],
  },
  integrations: [sitemap()],
  vite: {
    build: {
      chunkSizeWarningLimit: 600,
    },
  },
});


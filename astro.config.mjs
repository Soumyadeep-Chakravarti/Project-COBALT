import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";
import remarkGfm from "remark-gfm";
import rehypeSlug from "rehype-slug";

function remarkMermaid() {
  return function (tree) {
    console.log(
      "[remark-mermaid] Processing tree with",
      tree.children.length,
      "children",
    );
    tree.children.forEach((node, i) => {
      console.log(`[remark-mermaid] Child ${i}:`, node.type, node.lang || "");
      if (node.type === "code" && node.lang === "mermaid") {
        console.log("[remark-mermaid] Found mermaid at", i);
        const html = `<pre class="mermaid">${node.value}</pre>`;
        tree.children[i] = { type: "html", value: html };
      }
    });
  };
}

const base = process.env.BASE_URL || "/";

export default defineConfig({
  base,
  site: "https://cobalt.engineering",

  srcDir: "./src",
  outDir: "./dist",
  publicDir: "./public",

  image: {
    service: {
      entrypoint: "astro/assets/services/noop",
    },
  },
  markdown: {
    remarkPlugins: [[remarkMermaid], remarkGfm],
    rehypePlugins: [rehypeSlug],
  },
  integrations: [sitemap()],
  vite: {
    build: {
      chunkSizeWarningLimit: 600,
    },
  },
});


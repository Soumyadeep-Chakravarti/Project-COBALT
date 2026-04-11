import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const logs = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./docs/src/content/logs" }),
  schema: z.object({
    title: z.string(),
    date: z.date(),
    categories: z.array(z.string()).optional(),
    tags: z.array(z.string()).optional(),
    mermaid: z.boolean().optional(),
  }),
});

export const collections = { logs };
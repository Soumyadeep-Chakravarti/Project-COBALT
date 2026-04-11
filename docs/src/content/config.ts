import { defineCollection, z } from 'astro:content';

const logs = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date(),
    categories: z.array(z.string()).optional(),
    tags: z.array(z.string()).optional(),
    mermaid: z.boolean().optional(),
  }),
});

export const collections = { logs };
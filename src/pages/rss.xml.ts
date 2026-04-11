import rss from '@astrojs/rss';
import { getCollection, type CollectionEntry } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const base = context.base || '/Project-COBALT';
  const logs = await getCollection('logs');
  
  return rss({
    title: 'c0balt - dev logs',
    description: 'The cognitive core of a custom AR-based Operating System',
    site: context.site || 'https://soumyadeep-chakravarti.github.io',
    items: logs.map((log: CollectionEntry<'logs'>) => ({
      title: log.data.title,
      pubDate: log.data.date,
      description: log.body.slice(0, 200) + '...',
      link: `${base}/logs/${log.id}/`,
      categories: [...(log.data.categories || []), ...(log.data.tags || [])],
    })),
    customData: `<language>en-us</language>`,
  });
}

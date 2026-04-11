import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const logs = await getCollection('logs');
  
  return rss({
    title: 'c0balt - dev logs',
    description: 'The cognitive core of a custom AR-based Operating System',
    site: context.site || 'https://cobalt.engineering',
    items: logs.map((log) => ({
      title: log.data.title,
      pubDate: log.data.date,
      description: log.body.slice(0, 200) + '...',
      link: `/logs/${log.id}/`,
      categories: [...(log.data.categories || []), ...(log.data.tags || [])],
    })),
    customData: `<language>en-us</language>`,
    stylesheet: '/rss.xsl',
  });
}
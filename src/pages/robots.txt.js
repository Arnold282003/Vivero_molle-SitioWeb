import { ruta } from '../utils/rutas.js';

export function GET({ site }) {
  return new Response(
    `User-agent: *
Allow: /

Sitemap: ${new URL(ruta('sitemap.xml'), site).href}
`,
    { headers: { 'Content-Type': 'text/plain; charset=utf-8' } },
  );
}

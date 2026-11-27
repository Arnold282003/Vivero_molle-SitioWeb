import { ruta } from '../utils/rutas.js';

// Al añadir una página indexable, agrégala a esta lista.
const paginas = ['', 'catalogo/', 'nosotros/', 'contacto/'];

export function GET({ site }) {
  const urls = paginas
    .map((pagina) => `  <url><loc>${new URL(ruta(pagina), site).href}</loc></url>`)
    .join('\n');

  return new Response(
    `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>
`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
  );
}

import { defineConfig } from 'astro/config';

try {
  process.loadEnvFile(); // lee .env si existe
} catch {
  // Sin .env se usan los valores por defecto.
}

const env = process.env;
// Netlify expone la dirección pública del sitio en la variable URL.
const site = env.SITE_URL || (env.NETLIFY && env.URL) || 'https://www.molleytara.example';

export default defineConfig({
  site,
  base: env.BASE_PATH || '/',
  trailingSlash: 'always',
  build: { format: 'directory' },
  vite: {
    server: {
      // En desarrollo, /api se reenvía a Apache (XAMPP).
      proxy: {
        '/api': {
          target: env.PHP_BACKEND_URL || 'http://localhost/molle-y-tara',
          changeOrigin: true,
        },
      },
    },
  },
});

# Vivero Molle & Tara

Sitio web de un vivero en Pachacámac, Lima. Presenta el catálogo de plantas y servicios, la historia del negocio y un formulario de contacto.
https://arnold282003.github.io/Vivero_molle-SitioWeb/

## Características

- Cuatro páginas (Inicio, Catálogo, Nosotros y Contacto) y una página 404.
- Catálogo de 18 productos y servicios, con búsqueda que ignora tildes y filtro por categoría. El filtro se refleja en la URL.
- Formulario con validación en el navegador y en el servidor, consultas preparadas, campo trampa contra bots y límite de envíos.
- Diseño *mobile-first* con menú desplegable, navegación por teclado y buen contraste.
- SEO: títulos y descripciones por página, URL canónicas, Open Graph, `sitemap.xml`, `robots.txt` y datos estructurados `LocalBusiness`.
- Catálogo generado desde un CSV con validación previa.
- Ilustraciones SVG propias, sin fuentes ni recursos externos.

## Tecnologías

| Parte | Tecnología |
| --- | --- |
| Sitio estático | Astro |
| Interfaz | HTML5, CSS propio y JavaScript sin librerías |
| Formulario | PHP 8.1+ (PDO y mbstring) con MySQL o MariaDB |
| Datos e ilustraciones | Python 3.10+ (solo biblioteca estándar) |

## Estructura de carpetas

```text
.
├── .github/workflows/deploy.yml   Publicación en GitHub Pages
├── backend/
│   ├── api/
│   │   ├── contacto.php           Endpoint del formulario
│   │   ├── config.example.php     Plantilla de configuración
│   │   └── .htaccess              Protege la configuración en Apache
│   └── database/esquema.sql       Base de datos y tabla
├── data/productos.csv             Fuente del catálogo
├── public/                        Archivos que se copian tal cual
│   ├── favicon.svg
│   └── img/                       Ilustraciones e imagen para redes
├── scripts/
│   ├── generar_catalogo.py        CSV → JSON con validación
│   └── generar_ilustraciones.py   Dibuja los SVG
├── src/
│   ├── components/                Encabezado, pie y tarjeta
│   ├── data/
│   │   ├── catalogo.json          Generado: no editar a mano
│   │   └── negocio.js             Datos de contacto y horarios
│   ├── layouts/Base.astro         Plantilla común y SEO
│   ├── pages/                     Páginas, sitemap y robots
│   ├── scripts/                   Menú, catálogo y formulario
│   ├── styles/global.css
│   └── utils/
├── .env.example
├── astro.config.mjs
├── netlify.toml
└── package.json
```

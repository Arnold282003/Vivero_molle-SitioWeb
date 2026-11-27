# Vivero Molle & Tara

Sitio web de un vivero en Pachacámac, Lima. Presenta el catálogo de plantas y servicios, la historia del negocio y un formulario de contacto.

El sitio es estático (Astro). El formulario usa un endpoint en PHP que guarda los mensajes en MySQL.

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

## Instalación y ejecución

Los comandos se ejecutan desde la carpeta del proyecto.

### 1. Sitio (Astro)

Requiere Node.js 22.23.4 o superior (el archivo `.nvmrc` indica la versión 26).

```bash
npm install
npm run dev
```

El sitio queda en <http://localhost:4321>.

Para generar la versión de producción y revisarla:

```bash
npm run build
npm run preview
```

El resultado se guarda en `dist/`.

La configuración es opcional. Para cambiarla, copia `.env.example` como `.env`:

| Variable | Uso | Valor por defecto |
| --- | --- | --- |
| `SITE_URL` | Dominio para canónicas, Open Graph y sitemap | `https://www.molleytara.example` |
| `BASE_PATH` | Subcarpeta de publicación | `/` |
| `PUBLIC_CONTACT_ENDPOINT` | URL del endpoint PHP | `<BASE_PATH>api/contacto.php` |
| `PHP_BACKEND_URL` | Destino de `/api` durante `npm run dev` | `http://localhost/molle-y-tara` |

> El dominio `molleytara.example` y los datos de contacto son marcadores. Antes de publicar, define `SITE_URL` y actualiza `src/data/negocio.js`. El croquis (`mapa`) y la imagen para redes se dibujan en `scripts/generar_ilustraciones.py`.

### 2. Catálogo (Python)

Edita `data/productos.csv` (en UTF-8 y separado por comas) y ejecuta:

```bash
python scripts/generar_catalogo.py
```

En Windows también puedes usar `py` en lugar de `python`. Con `--solo-validar` se revisa el CSV sin escribir el JSON.

Si hay errores, el script los lista con su número de línea, termina con código 1 y conserva el JSON anterior.

| Columna | Regla |
| --- | --- |
| `id` | Único; minúsculas, números y guiones |
| `nombre` | De 3 a 60 caracteres |
| `categoria` | Una de las definidas en `CATEGORIAS`, dentro del script |
| `tipo` | `producto` o `servicio` (los servicios van en la categoría `Servicios`) |
| `precio` | Mayor que 0, con punto decimal (`35.50`) |
| `unidad` | De 3 a 40 caracteres; si termina en `desde`, se muestra antes del precio |
| `descripcion` | De 20 a 220 caracteres |
| `luz`, `riego` | Opcionales |
| `disponible`, `destacado` | `si` o `no`; el inicio muestra hasta 6 destacados disponibles |
| `imagen` | Archivo existente en `public/img/productos/` |
| `alt` | Descripción de la imagen, de 10 a 140 caracteres |

Las ilustraciones SVG se vuelven a generar con:

```bash
python scripts/generar_ilustraciones.py
```

Para un producto nuevo, coloca su imagen en `public/img/productos/` o añade una función de dibujo en ese script. La imagen para redes (`og-portada.png`, 1200×630) es una exportación de `og-portada.svg`; si cambias el dibujo, vuelve a exportarla.

Si añades una categoría, escribe también su resumen en `src/pages/index.astro`.

### 3. Formulario (PHP y MySQL con XAMPP)

1. Abre el panel de XAMPP e inicia **Apache** y **MySQL**.
2. Crea la base de datos. En <http://localhost/phpmyadmin>, abre la pestaña **Importar** y selecciona `backend/database/esquema.sql`.
3. Crea la carpeta `C:\xampp\htdocs\molle-y-tara\api` y copia dentro el contenido de `backend/api/`, incluido `.htaccess`.
4. En esa carpeta, copia `config.example.php` como `config.php` y completa el usuario y la clave de MySQL. En una instalación local de XAMPP sin cambios, el usuario es `root` y la clave está vacía; úsalo solo en tu equipo. Reemplaza también el valor de `sal`.

Con esto hay dos formas de probar.

**A. Con el servidor de desarrollo.** Ejecuta `npm run dev` y abre <http://localhost:4321/contacto/>. Astro reenvía `/api` a `http://localhost/molle-y-tara`. Si Apache usa otro puerto, ajusta `PHP_BACKEND_URL` en `.env`. Esta opción requiere `BASE_PATH=/`.

**B. Todo en Apache.** Define estas variables en `.env`:

```ini
SITE_URL=http://localhost
BASE_PATH=/molle-y-tara/
```

Ejecuta `npm run build`, copia el **contenido** de `dist/` en `C:\xampp\htdocs\molle-y-tara\` y abre <http://localhost/molle-y-tara/>. Quita o ajusta esas variables antes de compilar para producción.

Los mensajes recibidos se consultan en phpMyAdmin, en la tabla `molle_tara.mensajes_contacto`.

| Respuesta | Significado |
| --- | --- |
| 201 | Mensaje guardado |
| 403 | Origen no autorizado (revisa `origenes_permitidos`) |
| 405 / 413 | Método no permitido / envío demasiado grande |
| 422 | Datos no válidos, con el detalle por campo |
| 429 | Demasiados envíos en 10 minutos |
| 500 | Falta `config.php` o falló la base de datos (revisa el registro de errores de PHP) |

El campo trampa responde 200 sin guardar nada.

## Despliegue de la parte estática

GitHub Pages y Netlify **no ejecutan PHP**. Para que el formulario funcione, publica `backend/api/` en un hosting con PHP y MySQL (con HTTPS), crea allí la tabla y el `config.php`, y luego:

1. Añade el dominio del sitio estático a `origenes_permitidos`, sin barra final (por ejemplo, `https://usuario.github.io`).
2. Define `PUBLIC_CONTACT_ENDPOINT` con la URL completa de `contacto.php` y vuelve a compilar.

Sin ese paso el resto del sitio funciona, y el formulario muestra un aviso con el correo de contacto.

En un hosting compartido, si no puedes crear bases de datos por script, créala desde su panel e importa solo la sentencia `CREATE TABLE`.

### GitHub Pages

1. Sube el proyecto a un repositorio, en la rama `main`.
2. En **Settings → Pages → Source**, elige **GitHub Actions**.
3. Si tienes el endpoint PHP, crea la variable `PUBLIC_CONTACT_ENDPOINT` en **Settings → Secrets and variables → Actions → Variables**.
4. Haz un *push* a `main`, o ejecuta el flujo desde la pestaña **Actions**.

El flujo valida el CSV, calcula `SITE_URL` y `BASE_PATH`, compila y publica.

En un sitio de proyecto (`usuario.github.io/repositorio/`), los buscadores no leen el `robots.txt` de la subcarpeta. Envía el sitemap desde Google Search Console o usa un dominio propio.

### Netlify

1. Elige **Add new site → Import an existing project** y selecciona el repositorio.
2. Netlify toma el comando y la carpeta de `netlify.toml`, y la versión de Node de `.nvmrc`.
3. Si usas dominio propio o endpoint externo, define `SITE_URL` y `PUBLIC_CONTACT_ENDPOINT` en las variables de entorno. Sin `SITE_URL` se usa la dirección que asigna Netlify.

Netlify publica el JSON incluido en el repositorio, así que ejecuta el script de Python y confirma los cambios cuando edites el CSV.

## Antes de producción

- Completa los datos reales del negocio y el dominio.
- Usa un usuario de MySQL con permisos mínimos (ver el final de `esquema.sql`).
- Publica un aviso de privacidad acorde con la Ley N.º 29733 de Protección de Datos Personales y define cuánto tiempo conservarás los mensajes.

## Licencia

Distribuido bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE).

---
name: seo-optimizer
description: >
  Optimiza el SEO de una web estática multipágina añadiendo meta tags
  completos, Open Graph, Twitter Cards, Schema.org JSON-LD apropiado por
  tipo de página, favicon, sitemap.xml y robots.txt. Genera también la
  imagen OG (1200x630) si no existe. Usar cuando el usuario diga
  "optimiza SEO", "mejora el posicionamiento", "añade SEO", "preparar para
  Google", "schema markup", "open graph", o cualquier variante.
---

# SEO Optimizer

Optimización SEO completa para webs estáticas. Cubre las 4 áreas críticas:

1. **Meta tags por página** — title, description, canonical, robots
2. **Social sharing** — Open Graph + Twitter Cards
3. **Schema.org JSON-LD** — datos estructurados por tipo de página
4. **Site-wide** — sitemap.xml, robots.txt, favicon

---

## Datos que necesitas saber del proyecto

Antes de aplicar la skill, identifica:

- **Nombre de la empresa** (exacto)
- **URL de producción** (ej: `https://misitio.vercel.app` o dominio propio)
- **Tipo de negocio** (LocalBusiness, ProfessionalService, Restaurant, etc.)
- **Datos de contacto**: teléfono, email, dirección postal completa
- **Coordenadas geográficas** (lat/lng) si tiene local físico
- **Servicios principales** (listado)
- **Redes sociales** (Instagram, Facebook, etc.)

Si falta algún dato, marcarlo con `<!-- REVISAR -->`.

---

## Paso 1 — Meta tags por página

Reemplaza el `<head>` de cada HTML con esta estructura:

```html
<!DOCTYPE html>
<html lang="es-ES">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Title: 50-60 chars, incluir marca + propuesta + ubicación -->
  <title>Marca — Servicio en Ciudad | Diferenciador</title>

  <!-- Description: 120-155 chars, llamada a la acción -->
  <meta name="description" content="...">

  <meta name="keywords" content="kw1, kw2, kw3, ciudad">
  <meta name="author" content="Marca">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <link rel="canonical" href="https://midominio.com/pagina/">
  ...
</head>
```

**Reglas:**
- Cada página tiene su propio `<title>` y `<description>` únicos
- `canonical` apunta a la URL absoluta de esa página específica
- `noindex` solo para páginas internas (login, carrito, etc.)

---

## Paso 2 — Open Graph + Twitter Cards

Tras los meta básicos, añadir:

```html
<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:locale" content="es_ES">
<meta property="og:site_name" content="Marca">
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:url" content="https://midominio.com/pagina/">
<meta property="og:image" content="https://midominio.com/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="...">
<meta name="twitter:description" content="...">
<meta name="twitter:image" content="https://midominio.com/assets/og-image.jpg">
```

### Generar imagen OG (1200x630)

Si no existe, generar desde un asset visual del proyecto:

**Desde un vídeo (tomar frame):**
```bash
ffmpeg -i assets/hero.mp4 -ss 00:00:02 -vframes 1 \
  -vf "scale=1200:630:force_original_aspect_ratio=increase,crop=1200:630" \
  -y assets/og-image.jpg
```

**Desde una imagen grande:**
```bash
ffmpeg -i assets/foto-grande.jpg \
  -vf "scale=1200:630:force_original_aspect_ratio=increase,crop=1200:630" \
  -y assets/og-image.jpg
```

Tamaño objetivo: < 300KB.

---

## Paso 3 — Schema.org JSON-LD

Añadir un `<script type="application/ld+json">` por página, adaptado al tipo:

### En index.html — Organización + Sitio

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "ProfessionalService",
      "@id": "https://midominio.com/#organization",
      "name": "Marca",
      "description": "...",
      "url": "https://midominio.com/",
      "logo": "https://midominio.com/assets/logo.png",
      "telephone": "+34XXXXXXXXX",
      "email": "info@marca.com",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "Calle X, 1",
        "addressLocality": "Ciudad",
        "postalCode": "20009",
        "addressRegion": "Provincia",
        "addressCountry": "ES"
      },
      "geo": { "@type": "GeoCoordinates", "latitude": 0.0, "longitude": 0.0 },
      "areaServed": { "@type": "AdministrativeArea", "name": "Provincia" },
      "sameAs": ["https://instagram.com/marca"],
      "hasOfferCatalog": {
        "@type": "OfferCatalog",
        "itemListElement": [
          { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "Servicio 1" } }
        ]
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://midominio.com/#website",
      "url": "https://midominio.com/",
      "name": "Marca",
      "publisher": { "@id": "https://midominio.com/#organization" },
      "inLanguage": "es-ES"
    }
  ]
}
```

### En servicios.html — Catálogo de servicios

```json
{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "Servicios",
  "itemListElement": [
    {
      "@type": "Service",
      "position": 1,
      "name": "Servicio 1",
      "description": "...",
      "provider": { "@type": "ProfessionalService", "name": "Marca" }
    }
  ]
}
```

### En nosotros.html — AboutPage

```json
{
  "@context": "https://schema.org",
  "@type": "AboutPage",
  "name": "Sobre Marca",
  "mainEntity": { "@id": "https://midominio.com/#organization" }
}
```

### En contacto.html — ContactPage

```json
{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "name": "Contacto",
  "mainEntity": { "@id": "https://midominio.com/#organization" }
}
```

**Tipos de @type comunes:**
- `LocalBusiness` — comercio local genérico
- `ProfessionalService` — servicios profesionales (arquitectos, abogados, asesorías)
- `Restaurant`, `Hotel`, `Store` — comercios específicos
- `MedicalOrganization`, `Dentist` — sanitarios

---

## Paso 4 — Favicon

```html
<link rel="icon" type="image/png" href="assets/logo.png">
<link rel="apple-touch-icon" href="assets/logo.png">
```

Idealmente generar `favicon.ico` y `apple-touch-icon.png` (180x180) específicos.
Si no existe, usar el logo PNG como fallback.

---

## Paso 5 — sitemap.xml

Crear en la raíz del proyecto:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://midominio.com/</loc>
    <lastmod>2026-04-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://midominio.com/servicios.html</loc>
    <lastmod>2026-04-25</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- Una <url> por cada página -->
</urlset>
```

**Prioridades sugeridas:**
- Home: 1.0
- Servicios / productos principales: 0.8
- Sobre nosotros / blog: 0.6
- Contacto: 0.5
- Legales: 0.3

---

## Paso 6 — robots.txt

Crear en la raíz:

```
User-agent: *
Allow: /

Sitemap: https://midominio.com/sitemap.xml
```

Para bloquear ciertas rutas:
```
User-agent: *
Disallow: /admin/
Disallow: /api/
Allow: /
```

---

## Verificación post-deploy

Tras subir a producción:

1. **Google Search Console** — añadir propiedad y verificar
2. **Rich Results Test** — https://search.google.com/test/rich-results
3. **Facebook Debugger** — https://developers.facebook.com/tools/debug/
4. **Twitter Card Validator** — https://cards-dev.twitter.com/validator
5. **PageSpeed Insights** — https://pagespeed.web.dev/

Para indexación rápida: Search Console → Inspección de URL → Solicitar indexación.

---

## Errores comunes

| Síntoma | Solución |
|---|---|
| OG image no aparece en Facebook/WhatsApp | Forzar refresh en Facebook Debugger |
| Schema validation falla | Probar en Schema Markup Validator de Google |
| Canonical apunta a URL incorrecta | Verificar que coincide exactamente con la URL final tras redirects |
| Página no indexa | Comprobar `robots` meta y robots.txt — ¿hay `noindex`? |

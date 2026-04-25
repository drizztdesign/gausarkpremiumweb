---
name: web-rebuilder
description: >
  Usa esta skill cuando el usuario quiera reconstruir la web de un cliente
  a partir de su HTML original. Se activa con frases como: "usa la skill
  web-rebuilder", "reconstruye la web del cliente", "construye la web a
  partir del HTML original", "rehaz la web", "mejora la web existente",
  "haz una web nueva a partir de la original". También activar cuando haya
  un archivo HTML de origen en el proyecto (client-original.html,
  web-original.html) y el usuario pida construir o reconstruir la web.
---

# Web Rebuilder – Instrucciones para Claude

## Objetivo

Reconstruir la web de un cliente con diseño profesional y moderno,
conservando el 100% de sus contenidos reales. Nunca inventar información.
Nunca usar contenido placeholder.

---

## Paso 1 – Leer y extraer el contenido real

Lee el archivo `client-original.html` completo (en este proyecto se llama
`web-original.html`) y extrae:

- **Nombre de la empresa** (exacto, como aparece en la web)
- **Teléfono(s)** de contacto
- **Email(s)** de contacto
- **Dirección** física si aparece
- **Servicios** que ofrecen (lista completa, con nombres exactos)
- **Zonas o localidades** donde trabajan
- **Años de experiencia** u otros datos de confianza
- **Testimonios** de clientes si los hay
- **Precios** si aparecen
- **Colores principales** de la marca (en hex si es posible)
- **Tipografías** usadas si son relevantes
- **Slogan o frase principal**

Si algún dato no está claro, márcalo con `<!-- REVISAR -->` en el HTML
generado.

---

## Paso 2 – Estructura de páginas

Genera siempre estas 4 páginas:

1. **index.html** – Página principal
2. **servicios.html** – Todos los servicios detallados
3. **nosotros.html** – Historia, equipo, valores, confianza
4. **contacto.html** – Formulario, mapa, teléfono, email, dirección

---

## Paso 3 – Diseño y estructura de index.html

### Hero section

- Fondo oscuro semitransparente sobre el vídeo
- El vídeo `assets/hero.mp4` va en esta sección con el atributo
  `playsinline muted loop preload="auto"`
- Imagen de fallback: `assets/hero-poster.jpg`
- Marca la sección con el comentario `<!-- SCROLL-VIDEO-SECTION -->` para
  la skill scroll-video
- Título principal: nombre de la empresa en grande
- Subtítulo: slogan o frase principal
- Botón CTA principal: "Solicitar presupuesto" que enlaza a contacto.html
- Botón secundario: teléfono directo (tel:XXXXXXX)

### Secciones obligatorias en index.html

1. **Hero** con vídeo
2. **Por qué elegirnos** – 3 o 4 puntos de valor diferencial extraídos del
   contenido real
3. **Servicios principales** – tarjetas visuales con los servicios más
   importantes (máximo 6)
4. **Números de confianza** – años de experiencia, obras realizadas, zonas
   cubiertas (datos reales)
5. **Testimonios** – si existen en el HTML original
6. **CTA final** – sección de llamada a la acción con teléfono y botón de
   presupuesto
7. **Footer** – logo, navegación, teléfono, email, copyright

---

## Paso 4 – Reglas de diseño

### Lo que SÍ debes usar

- CSS propio en `<style>` dentro de cada HTML (sin archivos externos)
- Google Fonts vía CDN – elige una tipografía moderna y profesional (no
  Arial, no Roboto, no Inter genérico)
- Variables CSS para colores de marca (`--color-primary`, `--color-dark`,
  etc.)
- Diseño responsive con mobile-first
- Animaciones suaves con CSS (`transition`, `transform`)
- Grid y Flexbox para layouts

### Lo que NO debes usar

- Bootstrap, Tailwind CDN ni ningún framework CSS externo
- Imágenes de stock o placeholders (solo los assets reales del cliente)
- Contenido inventado – si no está en el HTML original, no lo pongas
- `Arial`, `Roboto` o `Inter` como tipografía principal (son demasiado
  genéricas)
- Efectos de scroll en el hero – eso lo gestiona la skill `scroll-video`
  después

### Estilo visual

- Diseño limpio, con mucho espacio en blanco
- Secciones con padding generoso (mínimo 80px arriba y abajo)
- Tarjetas con sombras suaves (`box-shadow`)
- Botones con bordes redondeados y hover con transición
- El color primario de la marca domina los CTAs, títulos y acentos
- Fondo del hero: negro semitransparente al 60% sobre el vídeo

---

## Paso 5 – Assets

- Logo: `assets/logo.png` – úsalo en el header y el footer
- Vídeo hero: `assets/hero.mp4`
- Poster del hero: `assets/hero-poster.jpg`
- Si hay imágenes adicionales en la web original, referenciarlas desde sus
  URLs originales

---

## Paso 6 – Navegación

Todas las páginas deben tener el mismo header y footer con:

- Logo enlazando a index.html
- Menú: Inicio | Servicios | Nosotros | Contacto
- Teléfono visible en el header (elemento clickable en móvil)
- Header sticky (que se quede fijo al hacer scroll)

---

## Paso 7 – Al terminar

Confirma al usuario:

- Los 4 archivos HTML generados
- Los contenidos reales que has extraído y usado
- Cualquier dato que hayas marcado con `<!-- REVISAR -->` porque no estaba
  claro
- Instrucciones para previsualizar: "Haz clic derecho en index.html →
  Open with Live Server"

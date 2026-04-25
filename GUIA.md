# Guía de construcción — gausarkpremiumweb

Bitácora cronológica de cómo se construyó esta web. Cada entrada documenta una acción concreta, su motivación y los archivos afectados.

## Stack y decisiones generales

**Cliente / marca:** Gausark S.L.P. — estudio de arquitectura y diseño con más de 40 años de experiencia, con sede en Donostia (Txapillo Kalea 3, bajo izq, 20009 Gipuzkoa).

**Contacto público:** gausarksl@gausark.es · 943 44 07 52 · Instagram @gausarksl

**Idiomas de la web:** español (principal), euskera, inglés.

**Estructura actual del sitio (menú):** gausark · proyectos · noticias · contacto.

**Stack del sitio original (el que vamos a reemplazar/mejorar):**
- WordPress 5.4.1 con tema **Kleanity** (y child theme `kleanity-child`)
- Plugin visual **Goodlayers Core** (page builder)
- **Slider Revolution 6.2.22** para el slider de portada
- **Contact Form 7** para formularios
- **Yoast SEO** para metadatos
- Google Analytics vía MonsterInsights (UA-187468060-1)
- Cookiebot para consentimiento
- Tipografías: Poppins + Nunito (Google Fonts)

**Objetivo del proyecto `gausarkpremiumweb`:** crear una versión mejorada ("premium") de la web de Gausark, partiendo del HTML actual como referencia y reemplazando el stack pesado de WordPress + plugins por algo más moderno y liviano (a decidir).

## 1. Decisiones iniciales

### 2026-04-24 — Capturar el sitio actual como línea base

**Qué:** Guardé el HTML renderizado de `https://gausark.com/` (vía "Ver código fuente" del navegador) en `web-original.html`, y añadí el logotipo actual `Logotipo-Gaursark.png` a la raíz del proyecto.
**Por qué:** Tener la versión actual congelada como referencia antes de mejorarla. Así siempre podemos volver a ver qué había (contenidos, textos, estructura, assets) y comparar el "antes / después" de cada mejora. El HTML capturado incluye todos los scripts inline de WordPress/Slider Revolution/Analytics; lo dejamos tal cual aunque no se vaya a ejecutar fuera del servidor original.
**Cómo:** Pegar el view-source completo en `web-original.html` y copiar el logo a la raíz.
**Archivos:** web-original.html, Logotipo-Gaursark.png

## 2. Setup del proyecto


## 3. Estructura y arquitectura

### 2026-04-24 — Generar las 4 páginas HTML con skill web-rebuilder

**Qué:** Generé las 4 páginas de la web a partir del contenido real extraído de `web-original.html`. Diseño nuevo, limpio y premium desde cero — sin reutilizar el código WordPress original.
**Por qué:** La web original era WordPress + Kleanity + plugins pesados. La reconstrucción es HTML+CSS+JS puro, sin dependencias, mobile-first, con tipografía premium y diseño de estudio de arquitectura.
**Cómo:** Skill `web-rebuilder` — extracción de contenido real + generación de 4 páginas con CSS inline, Google Fonts (Cormorant Garamond + Nunito), variables CSS, hero con vídeo, header sticky, menú hamburguesa.
**Archivos:** index.html, servicios.html, nosotros.html, contacto.html

**Contenido real extraído y usado:**
- Nombre: Gausark S.L.P.
- Teléfono: 943 44 07 52
- Email: gausarksl@gausark.es
- Dirección: Txapillo Kalea, 3, bajo izq · 20009 Donostia, Gipuzkoa
- Servicios confirmados: Obra nueva, Reformas, Rehabilitación
- Experiencia: +40 años
- Social: Instagram @gausarksl
- Legal: Aviso legal, Política de privacidad, Política de cookies

**Datos marcados como `<!-- REVISAR -->`:**
- Número de proyectos realizados
- Año de fundación exacto e historia del estudio
- Servicios adicionales (diseño interior, ITE, consultoría energética...)
- Miembros del equipo (nombres, cargos, fotos)
- Slogan o frase principal del estudio
- Foto fallback del hero (`assets/hero-poster.jpg` — pendiente de añadir)
- Fotos reales para servicios.html y nosotros.html
- ID de Formspree para el formulario de contacto (`YOUR_FORM_ID`)
- URL exacta del embed de Google Maps

## 4. Diseño y UI

### 2026-04-24 — Vídeo del hero se activa al hacer scroll (no autoplay)

**Qué:** Eliminé el atributo `autoplay` del vídeo hero. Ahora arranca solo cuando el usuario hace el primer scroll, mostrando el poster estático mientras no hay interacción.
**Por qué:** El autoplay inmediato distrae. Que el movimiento empiece al hacer scroll da una sensación más cinematográfica y premium, más acorde con un estudio de arquitectura.
**Cómo:** Quitar `autoplay`, añadir `id="heroVideo"` y listener de scroll que llama a `heroVideo.play()` una sola vez y se elimina.
**Archivos:** index.html

### 2026-04-24 — Organizar carpeta assets/ con vídeo y logo

**Qué:** Creé la carpeta `assets/`, moví el vídeo renombrándolo a `hero.mp4` (convención de la skill `web-rebuilder`) y copié el logotipo como `logo.png`. Dos fotos de obras reales de Gausark (edificio residencial terminado + obra en construcción con grúas) están pendientes de añadir — irán como `hero-poster.jpg` (fallback del vídeo) y `foto-construccion.jpg` para el efecto de scroll del hero.
**Por qué:** La skill `web-rebuilder` espera los assets en `assets/` con nombres fijos (`hero.mp4`, `hero-poster.jpg`, `logo.png`). Organizarlo ahora evita referencias rotas cuando se generen los HTML.
**Cómo:** `mkdir assets/`, `mv video → assets/hero.mp4`, `cp Logotipo-Gaursark.png → assets/logo.png`
**Archivos:** assets/hero.mp4 (18 MB), assets/logo.png — pendiente: assets/hero-poster.jpg, assets/foto-construccion.jpg

### 2026-04-24 — Crear skill web-rebuilder

**Qué:** Creé la skill `web-rebuilder` en `.claude/skills/web-rebuilder/SKILL.md`. Reconstruye la web de un cliente a partir de su HTML original generando 4 páginas (index, servicios, nosotros, contacto) con contenido 100% real extraído del HTML, hero con vídeo, CSS propio, tipografía premium y mobile-first.
**Por qué:** Skill transcrita desde comando existente, corrigiendo el trigger demasiado estrecho y añadiendo referencia al nombre de archivo `web-original.html` propio de este proyecto.
**Archivos:** .claude/skills/web-rebuilder/SKILL.md

## 5. Contenido y datos

## 6. Integraciones externas

## 7. Funcionalidades

## 8. Performance y SEO

## 9. Deploy e infraestructura

## 10. Mantenimiento y notas

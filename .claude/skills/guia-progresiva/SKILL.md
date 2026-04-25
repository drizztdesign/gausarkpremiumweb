---
name: guia-progresiva
description: Use SIEMPRE cuando se haga cualquier acción de desarrollo en el proyecto gausarkpremiumweb — crear o editar archivos, instalar dependencias, configurar herramientas, diseñar componentes, escribir estilos, conectar APIs, hacer deploy, decisiones de arquitectura. La skill agrega una entrada estructurada al archivo GUIA.md de la raíz para construir incrementalmente una guía cronológica de cómo se construyó la web. Activar también cuando el usuario diga "anotá esto", "registrá", "agregá a la guía", o cuando termine un hito notable. ADEMÁS, activar cuando el usuario indique que el proyecto está terminado ("ya está todo hecho", "ya terminé", "está finalizado", "ya está listo") — en ese caso, exportar GUIA.md a GUIA.pdf para uso en futuros proyectos. NO activar para preguntas, exploración de código, o acciones puramente de lectura.
---

# Guía Progresiva del Proyecto

Vas construyendo, junto al usuario, el sitio **gausarkpremiumweb**. Tu trabajo paralelo es mantener un documento `GUIA.md` en la raíz del proyecto que sirva como **bitácora viva**: qué se hizo, por qué, con qué comandos y qué archivos quedaron tocados. La idea es que dentro de unas semanas el usuario (o cualquiera) pueda leer `GUIA.md` y reconstruir mentalmente el camino completo que llevó a la web final.

## Cuándo agregar una entrada

Después de hacer (no antes) una acción significativa. "Significativa" significa que dejó un cambio observable en el proyecto o en el entorno:

- Crear archivos o carpetas nuevas
- Editar archivos de configuración (package.json, tsconfig, vite.config, .env, etc.)
- Instalar, actualizar o quitar dependencias
- Inicializar herramientas (git, framework, linter, formateador, base de datos)
- Diseñar o modificar un componente, página o estilo visible
- Conectar una API, servicio externo, o base de datos
- Configurar deploy, hosting, dominio, CI
- Tomar una decisión de arquitectura o stack que afecte cómo se construye lo demás

**Cuándo NO agregar entrada:**

- Leer archivos para entender contexto
- Responder preguntas del usuario sin tocar nada
- Búsquedas y exploración (Grep, Glob)
- Intentos fallidos que se revirtieron sin dejar rastro
- Cambios triviales que el usuario va a deshacer en el siguiente turno (en duda, esperá)

Si tenés duda razonable de si algo amerita entrada: agregala. Es más útil un GUIA.md con alguna entrada de más que uno con huecos.

## Cómo agregar una entrada

1. **Leé `GUIA.md`** primero. Si no existe, creálo con la plantilla de abajo. Si existe, identificá la **fase** correcta (ver lista) y agregá la entrada al final de esa fase.
2. **No dupliques**: si la entrada que ibas a escribir ya existe casi igual (mismo archivo, misma acción, mismo día), actualizá la existente en vez de duplicar.
3. **Append, no reescribas**: respetá lo que el usuario ya tenga ahí, incluso si está desordenado.

### Estructura de una entrada

```markdown
### YYYY-MM-DD — Título corto en imperativo

**Qué:** Una o dos frases describiendo el cambio concreto.
**Por qué:** Motivación — qué problema resuelve, qué decisión hay detrás.
**Cómo:** Comando ejecutado o resumen de la edición. Si fueron varios pasos, lista corta.
**Archivos:** Rutas relativas tocadas, separadas por coma. Si son muchos, agrupá por carpeta.
```

Mantené cada campo en una línea cuando se pueda. Si "Por qué" es obvio (ej. "instalé React porque es un proyecto React"), podés omitir esa línea — pero el "Por qué" suele ser lo más valioso a futuro, así que en duda escribilo.

### Fases

`GUIA.md` se organiza por fases en este orden. Si una fase todavía no tiene entradas, no creés la sección hasta que haga falta.

1. **Decisiones iniciales** — stack, objetivos, qué tipo de web, restricciones
2. **Setup del proyecto** — init, git, framework base, dependencias core
3. **Estructura y arquitectura** — carpetas, rutas, layouts, convenciones
4. **Diseño y UI** — sistema de diseño, componentes, estilos, assets
5. **Contenido y datos** — modelos, fuentes de datos, CMS, APIs propias
6. **Integraciones externas** — APIs de terceros, auth, pagos, analytics
7. **Funcionalidades** — features de usuario concretas
8. **Performance y SEO** — optimizaciones, metadatos, accesibilidad
9. **Deploy e infraestructura** — hosting, dominio, CI/CD, variables de entorno
10. **Mantenimiento y notas** — bugs encontrados, decisiones revertidas, deuda técnica

Si una acción cae claramente entre dos fases, elegí la más temprana en la lista.

## Plantilla inicial de GUIA.md

Cuando creés el archivo por primera vez, usá exactamente esto:

```markdown
# Guía de construcción — gausarkpremiumweb

Bitácora cronológica de cómo se construyó esta web. Cada entrada documenta una acción concreta, su motivación y los archivos afectados.

## Stack y decisiones generales

_(se completa a medida que se toman decisiones)_

## 1. Decisiones iniciales

## 2. Setup del proyecto

## 3. Estructura y arquitectura

## 4. Diseño y UI

## 5. Contenido y datos

## 6. Integraciones externas

## 7. Funcionalidades

## 8. Performance y SEO

## 9. Deploy e infraestructura

## 10. Mantenimiento y notas
```

A medida que uses una fase por primera vez, dejá la siguiente entrada bajo su encabezado.

## Ejemplo de entrada bien hecha

```markdown
### 2026-04-24 — Inicializar proyecto Next.js con TypeScript

**Qué:** Creé el scaffold base con `create-next-app` usando App Router y Tailwind.
**Por qué:** Next.js da SSR y rutas listas, y Tailwind acelera el diseño visual sin pelearse con CSS modules.
**Cómo:** `npx create-next-app@latest . --typescript --tailwind --app --eslint`
**Archivos:** package.json, tsconfig.json, next.config.js, tailwind.config.ts, app/layout.tsx, app/page.tsx
```

## Ejemplo de entrada mediocre (evitá esto)

```markdown
### 2026-04-24 — Cambios

Hice cosas en el proyecto.
```

Sin "qué", sin "por qué", sin archivos — inútil dentro de tres semanas.

## Cómo encajar esto en tu flujo

No interrumpas la conversación con el usuario para anunciar cada anotación. El patrón es:

1. Hacés lo que el usuario pidió (crear archivo, instalar lib, etc.)
2. Antes de cerrar el turno, agregás la entrada a `GUIA.md` en silencio
3. En tu mensaje final mencionás brevemente que actualizaste la guía: una sola línea, ej. _"Anoté el setup en GUIA.md bajo Setup del proyecto."_

Si el usuario hace varias cosas en un mismo turno, podés agrupar en una sola entrada con `Cómo:` en lista, en vez de fragmentar.

## Finalización — exportar a PDF

Cuando el usuario diga que el proyecto está terminado (frases típicas: _"ya está todo hecho"_, _"ya terminé"_, _"está finalizado"_, _"ya está listo"_, _"cerralo"_), tu trabajo final es convertir `GUIA.md` en `GUIA.pdf` para que el usuario lo lleve como referencia a futuros proyectos.

### Pasos

1. **Releé `GUIA.md` completo** y verificá que esté coherente: secciones en orden, sin entradas duplicadas, sin TODOs sueltos. Si encontrás huecos obvios, preguntá al usuario antes de generar el PDF.
2. **Agregá una sección final** al markdown con un breve resumen de aprendizajes — qué funcionó, qué no, qué haría distinto. Algo así:

   ```markdown
   ## Aprendizajes para futuros proyectos

   - _(3 a 6 bullets, derivados de las entradas de Mantenimiento y notas y de las decisiones más impactantes)_
   ```

3. **Generá el PDF** usando el script `scripts/export_pdf.py`:

   ```bash
   python .claude/skills/guia-progresiva/scripts/export_pdf.py
   ```

   El script intenta varios métodos en orden y usa el primero disponible. Si todos fallan, te dirá qué instalar.

4. **Confirmá al usuario** dónde quedó el PDF (raíz del proyecto, `GUIA.pdf`) y mencioná brevemente qué método se usó para generarlo, por si quiere ajustar el estilo.

### Si el script falla

- Si pandoc no está instalado y el usuario quiere instalarlo: en Windows con winget → `winget install JohnMacFarlane.Pandoc`. Con Chocolatey → `choco install pandoc`.
- Como fallback sin instalar nada: el script puede generar `GUIA.html` con estilos listos para imprimir. Avisale al usuario que abra ese HTML en el navegador y use _Imprimir → Guardar como PDF_.

## Cuando el usuario corrija o revierta

Si en un turno posterior el usuario revierte algo que ya anotaste, **no borres la entrada original** — agregá una nota corta debajo:

```markdown
> Revertido el 2026-04-26: ver entrada en _Mantenimiento y notas_.
```

Y en _Mantenimiento y notas_ agregá la entrada de reversión con su "Por qué". La idea es que la guía cuente la historia real, incluyendo callejones sin salida — eso es lo que hace que sea útil para aprender, no solo un changelog limpio.

---
name: scroll-video
description: >
  Hace que el vídeo hero de una web esté ligado a la posición del scroll:
  el vídeo avanza/retrocede siguiendo al scroll, y la velocidad de la
  transición depende de cuán rápido scrolea el usuario. Bloquea el scroll
  hacia abajo hasta que el vídeo ha terminado. Usar cuando el usuario diga
  "que el vídeo avance con el scroll", "scroll-driven video", "el vídeo
  controlado por scroll", "que no pueda bajar hasta que termine el vídeo",
  o cualquier variante. El HTML debe tener <!-- SCROLL-VIDEO-SECTION -->
  marcando la sección hero.
---

# Scroll Video

**Approach definitivo (validado con cliente real, 2026-04-26):** pre-renderizar cada frame del vídeo a un `ImageBitmap` al cargar, sustituir el `<video>` por un `<canvas>`, y dibujar el frame correspondiente al scroll con `ctx.drawImage(bitmap)`. Operación GPU instantánea, sin decodificación de vídeo durante el scroll. Imposible que tartamudee.

## Por qué este approach gana a todo lo demás

Probé las 4 alternativas con un cliente real. Solo una funciona perfecto:

| Approach | Resultado |
|---|---|
| `video.play()` con `playbackRate` variable | Saltos en backward, snap final, no sigue scroll real. **Fail.** |
| `currentTime` directo (sin lerp) | Saltos teleport en scroll rápido. **Fail.** |
| `currentTime` con rAF lerp continuo | Decoder no cachea frames decodificados → primer scrub a trompicones, mejora con repetición. **Fail.** |
| `currentTime` con rAF lerp + prewarm (fetch + seek-sampling) | Igual: decoder descarta cada frame al seekar al siguiente. Pre-calentar 60 puntos no sirve. **Fail.** |
| **Canvas + ImageBitmap[]** | Decode upfront una vez, scroll dibuja bitmaps GPU. **Perfecto.** |

> **Lección clave:** los browsers NO mantienen un caché de frames decodificados entre seeks. Cada `video.currentTime = X` decodifica un frame y descarta el anterior. Por eso pre-seekear no calienta nada — al terminar el pre-seek, solo el último frame está en memoria. La única forma de eliminar el problema es sacar la decodificación del scroll-time: pre-renderizar todos los frames a `ImageBitmap` al cargar (fuera del decoder de vídeo, en memoria GPU permanente) y usar canvas en vez de video durante el scroll.

---

## 1. Encoding (recomendado pero no crítico con canvas approach)

Con el canvas approach, el encoding del vídeo importa solo para la fase de captura inicial. Aún así, recomendado re-encodar con keyframe-per-frame para que los seeks de captura sean rápidos:

```bash
ffmpeg -i hero.mp4 \
  -c:v libx264 -x264opts "keyint=1:min-keyint=1:no-scenecut" \
  -crf 23 -preset slow -tune film \
  -an -movflags +faststart \
  -y hero-scrub.mp4

ffmpeg -i hero.mp4 \
  -c:v libx264 -x264opts "keyint=1:min-keyint=1:no-scenecut" \
  -crf 24 -preset slow -tune film \
  -vf "scale=1280:-2" -an -movflags +faststart \
  -y hero-scrub-mobile.mp4
```

**Extraer poster** (se muestra durante la captura, ~3-5s):
```bash
ffmpeg -ss 00:00:01 -i hero-scrub.mp4 -frames:v 1 -q:v 2 hero-poster.jpg
```

---

## 2. HTML

```html
<!-- SCROLL-VIDEO-SECTION -->
<div class="scroll-video-wrapper">
  <section class="hero">
    <div class="hero-poster-bg" aria-hidden="true"></div>
    <video id="heroVideo" muted playsinline preload="auto" poster="assets/hero-poster.jpg">
      <source src="assets/hero-scrub-mobile.mp4" type="video/mp4" media="(max-width: 768px)">
      <source src="assets/hero-scrub.mp4" type="video/mp4">
    </video>
    <!-- el JS inserta <canvas class="hero-canvas"> aquí dinámicamente -->
    <div class="hero-overlay"></div>
    <div class="hero-content"><!-- texto, CTA, etc. --></div>
  </section>
</div>
```

Sin `autoplay` ni `loop`. El JS los activa solo en móvil.

---

## 3. CSS

```css
.scroll-video-wrapper { height: 175vh; }
.scroll-video-wrapper .hero { position: sticky; top: 0; height: 100vh; }
@media (max-width: 768px) {
  .scroll-video-wrapper { height: auto; }
  .scroll-video-wrapper .hero { position: relative; }
}

/* Vídeo: oculto permanentemente en desktop. Solo se usa para CAPTURAR
   los frames al inicio. En móvil sí se ve y reproduce en autoplay loop. */
.hero video {
  position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
  opacity: 0; visibility: hidden; pointer-events: none;
  z-index: 1;
}

/* Canvas que sustituye al vídeo durante el scroll */
.hero-canvas {
  position: absolute; inset: 0; width: 100%; height: 100%;
  object-fit: cover;
  opacity: 0; transition: opacity .5s ease;
  z-index: 1; pointer-events: none; display: block;
}
.hero-canvas.ready { opacity: 1; }

/* Poster mostrado mientras se renderizan los frames a memoria (3-5s) */
.hero-poster-bg {
  position: absolute; inset: 0;
  background-image: url('assets/hero-poster.jpg');
  background-size: cover; background-position: center;
  transition: opacity .5s ease;
  z-index: 0;
}
.hero-poster-bg.faded { opacity: 0; pointer-events: none; }

.hero-overlay { z-index: 2; }
.hero-content { z-index: 3; position: relative; }

/* En móvil mostramos el vídeo normal con autoplay loop */
@media (max-width: 768px) {
  .hero video { opacity: 1; visibility: visible; }
  .hero-canvas, .hero-poster-bg { display: none; }
}
```

---

## 4. JS completo (canvas + ImageBitmap)

```javascript
// MÓVIL: bypass scroll-driven (autoplay loop simple — Safari iOS no escala)
(function () {
  var video = document.getElementById('heroVideo');
  if (!video) return;
  if (window.matchMedia('(max-width: 768px)').matches) {
    video.setAttribute('autoplay', '');
    video.setAttribute('loop', '');
    video.muted = true;
    video.loop = true;
    video.play().catch(function () {});
    return;
  }
}());

// DESKTOP: canvas approach
// 1. fetch() del vídeo a memoria como Blob URL → seeks instantáneos
// 2. Seek frame por frame → drawImage(video) → createImageBitmap → push a frames[]
// 3. Hide video, show canvas
// 4. Scroll handler: drawImage(frames[idx]) → operación GPU instantánea
(function () {
  if (window.matchMedia('(max-width: 768px)').matches) return;
  var video       = document.getElementById('heroVideo');
  var wrapper     = document.querySelector('.scroll-video-wrapper');
  var placeholder = document.querySelector('.hero-poster-bg');
  if (!video || !wrapper) return;

  var ready    = false;
  var complete = false;
  var rafId    = null;
  var current  = 0;        // índice de frame actual (no segundos)
  var LERP     = 0.18;     // 0.10 cinematográfico · 0.18 balanceado · 0.30 reactivo
  var frames   = [];       // ImageBitmap[]
  var canvas   = null;
  var ctx      = null;

  function wrapTop() { return wrapper.getBoundingClientRect().top + window.scrollY; }
  function range()   { return Math.max(1, wrapper.offsetHeight - window.innerHeight); }
  function targetIndex() {
    if (!frames.length) return 0;
    var scrolled = Math.max(0, window.scrollY - wrapTop());
    var p = Math.min(1, scrolled / range());
    return p * (frames.length - 1);
  }
  function drawFrame(idx) {
    if (!ctx) return;
    idx = Math.max(0, Math.min(frames.length - 1, idx | 0));
    var bmp = frames[idx];
    if (bmp) ctx.drawImage(bmp, 0, 0, canvas.width, canvas.height);
  }

  function tick() {
    if (!ready || !frames.length) { rafId = null; return; }
    var target = targetIndex();
    var diff   = target - current;
    // Lerp adaptativo: si diff > 4 frames (scroll rápido), aceleramos
    var k = Math.abs(diff) > 4 ? Math.min(0.5, LERP + Math.abs(diff) * 0.02) : LERP;
    if (Math.abs(diff) < 0.05) {
      current = target;
      drawFrame(Math.round(current));
      if (current >= frames.length - 1.05) complete = true;
      rafId = null;
      return;
    }
    current += diff * k;
    drawFrame(Math.round(current));
    rafId = requestAnimationFrame(tick);
  }

  function onScroll() {
    if (!ready || !frames.length) return;
    if (!rafId) rafId = requestAnimationFrame(tick);
  }

  function finishPrewarm() {
    if (ready) return;
    ready = true;
    drawFrame(0);
    if (canvas) canvas.classList.add('ready');
    if (placeholder) placeholder.classList.add('faded');
    try { video.style.display = 'none'; } catch (_) {}
    onScroll();
  }

  function setupCanvas(w, h) {
    canvas = document.createElement('canvas');
    canvas.className = 'hero-canvas';
    canvas.width = w;
    canvas.height = h;
    canvas.setAttribute('aria-hidden', 'true');
    ctx = canvas.getContext('2d');
    video.parentNode.insertBefore(canvas, video.nextSibling);
  }

  function captureFrames() {
    return new Promise(function (resolve) {
      // Escala del bitmap respecto al vídeo nativo. 0.6 = balance bueno.
      // 1920x1080 → 1152x648 × 4 bytes × 121 frames ≈ 360MB en GPU.
      var SCALE = 0.6;
      var w = Math.max(2, Math.floor(video.videoWidth * SCALE));
      var h = Math.max(2, Math.floor(video.videoHeight * SCALE));
      var fps = 24;
      var totalFrames = Math.max(1, Math.round(video.duration * fps));
      var MAX_FRAMES = 200; // cap por seguridad de memoria
      var stride = Math.max(1, Math.ceil(totalFrames / MAX_FRAMES));
      var captureCount = Math.ceil(totalFrames / stride);

      var off = document.createElement('canvas');
      off.width = w; off.height = h;
      var offctx = off.getContext('2d');
      setupCanvas(w, h);

      var i = 0;
      function nextFrame() {
        if (i >= captureCount) { resolve(); return; }
        var t = (i * stride) / fps;
        if (t >= video.duration) t = Math.max(0, video.duration - 0.001);
        i++;

        var captured = false;
        function capture() {
          if (captured) return;
          captured = true;
          try {
            offctx.drawImage(video, 0, 0, w, h);
            if (window.createImageBitmap) {
              createImageBitmap(off).then(function (bmp) {
                frames.push(bmp);
                // Yield al event loop cada 10 frames para no bloquear UI
                if (i % 10 === 0) setTimeout(nextFrame, 0); else nextFrame();
              }).catch(function () {
                // Fallback: copiar a canvas dedicado (más memoria)
                var copy = document.createElement('canvas');
                copy.width = w; copy.height = h;
                copy.getContext('2d').drawImage(off, 0, 0);
                frames.push(copy);
                nextFrame();
              });
            } else {
              var copy = document.createElement('canvas');
              copy.width = w; copy.height = h;
              copy.getContext('2d').drawImage(off, 0, 0);
              frames.push(copy);
              nextFrame();
            }
          } catch (e) { nextFrame(); }
        }

        // requestVideoFrameCallback es la API correcta para esperar a que
        // el frame realmente esté pintado. Fallback a 'seeked' si no existe.
        var safety = setTimeout(capture, 300);
        if (video.requestVideoFrameCallback) {
          video.requestVideoFrameCallback(function () {
            clearTimeout(safety);
            requestAnimationFrame(capture); // 1 rAF más para asegurar paint
          });
        } else {
          video.addEventListener('seeked', function onseek() {
            video.removeEventListener('seeked', onseek);
            clearTimeout(safety);
            requestAnimationFrame(capture);
          });
        }
        try { video.currentTime = t; } catch (_) { capture(); }
      }
      nextFrame();
    });
  }

  function prewarm() {
    if (!video.videoWidth || !video.duration) {
      video.addEventListener('loadedmetadata', prewarm, { once: true });
      return;
    }
    // Determinar URL real según media queries del <source>
    var url = null;
    var sources = video.querySelectorAll('source');
    for (var i = 0; i < sources.length; i++) {
      var s = sources[i];
      if (!s.media || window.matchMedia(s.media).matches) { url = s.src; break; }
    }
    if (!url) url = video.currentSrc;

    function afterFile() {
      captureFrames().then(finishPrewarm).catch(finishPrewarm);
    }

    if (!url) { afterFile(); return; }

    // fetch() del archivo entero a Blob → todos los seeks de captura serán
    // instantáneos porque el archivo está en memoria, no requieren red
    fetch(url).then(function (r) {
      if (!r.ok) throw new Error('fetch failed');
      return r.blob();
    }).then(function (blob) {
      var blobUrl = URL.createObjectURL(blob);
      while (video.firstChild) video.removeChild(video.firstChild);
      video.src = blobUrl;
      return new Promise(function (resolve, reject) {
        var to = setTimeout(reject, 12000);
        video.addEventListener('loadedmetadata', function () {
          clearTimeout(to); resolve();
        }, { once: true });
      });
    }).then(afterFile).catch(afterFile);
  }

  // Bloquear scroll desktop hasta que el vídeo termine (current llega al final)
  window.addEventListener('wheel', function (e) {
    if (complete || !ready || !frames.length || e.deltaY <= 0) return;
    var wrapperEnd = wrapTop() + range();
    if (window.scrollY + e.deltaY > wrapperEnd && current < frames.length - 2) {
      e.preventDefault();
    }
  }, { passive: false });

  var touchStartY = 0;
  window.addEventListener('touchstart', function (e) {
    touchStartY = e.touches[0].clientY;
  }, { passive: true });
  window.addEventListener('touchmove', function (e) {
    if (complete || !ready || !frames.length) return;
    var dy = touchStartY - e.touches[0].clientY;
    if (dy <= 0) return;
    var wrapperEnd = wrapTop() + range();
    if (window.scrollY + dy > wrapperEnd && current < frames.length - 2) {
      e.preventDefault();
    }
  }, { passive: false });

  window.addEventListener('scroll', onScroll, { passive: true });
  prewarm();
}());
```

---

## Flujo completo (visualización)

1. **Página carga.** Hero muestra `.hero-poster-bg` (imagen estática, opacity:1). Vídeo `opacity:0 visibility:hidden`. Canvas todavía no existe.
2. **`prewarm()` arranca:** fetch() del archivo del vídeo → Blob URL → re-asigna a `video.src`.
3. **`captureFrames()`:** crea canvas e inicia bucle. Para cada frame: `video.currentTime = t`, espera `requestVideoFrameCallback`, `offctx.drawImage(video)`, `createImageBitmap(off)` → push a `frames[]`.
4. **Cuando termina** (~3-5s para vídeo de 5s): `finishPrewarm()`. Canvas fade-in, poster fade-out, video display:none.
5. **Usuario scrollea:** `tick()` calcula `targetIndex` desde scroll, lerpa `current` hacia él, `drawFrame(Math.round(current))` dibuja `frames[idx]` al canvas.
6. **Bloqueo de scroll** mientras `current < frames.length - 2` y dentro del wrapper.

---

## Ajustes

| Qué | Dónde | Efecto |
|---|---|---|
| Reactividad del lerp | `var LERP = 0.18` | 0.10 cinematográfico, 0.30 reactivo |
| Umbral lerp adaptativo | `Math.abs(diff) > 4` | (en frames) Si subes a 8, solo acelera con scroll muy rápido |
| Cap del lerp adaptativo | `Math.min(0.5, ...)` | Cuánto puede subir como máximo |
| Escala del bitmap | `var SCALE = 0.6` | 0.6 ≈ 360MB para 121 frames 1080p. Bajar a 0.5 = 250MB. Subir a 0.75 = 560MB |
| Cap de frames | `var MAX_FRAMES = 200` | Si el vídeo es muy largo, samplea 1 de cada N frames |
| Duración del scroll | `175vh` en CSS | Menos = transición más corta |
| Tolerancia bloqueo | `current < frames.length - 2` | Margen de 2 frames antes del final |

---

## Notas

- **Memoria:** ~360MB para vídeo 5s @ 24fps a 1080p con SCALE=0.6. Aceptable en desktop. Mobile usa autoplay loop, no canvas.
- **Tiempo de prewarm:** 1-2s fetch + 2-3s captura ≈ 3-5s total. Usuario ve el poster mientras tanto.
- **CORS:** el fetch funciona en mismo origen. Si sirves el vídeo desde un CDN distinto al de la página, asegúrate de que envíe `Access-Control-Allow-Origin: *`.
- **`.hero-placeholder` legacy:** si tu base CSS premium tiene `.hero-placeholder { display: none }`, ignóralo o usa `.hero-poster-bg` como en este skill.
- **Tamaño del archivo de vídeo no es crítico** para fluidez del scroll porque el archivo se descarga UNA vez y los frames están en memoria. Lo crítico es la memoria GPU para los bitmaps.
- Si el vídeo es **muy corto** (~2s), reducir SCALE a 0.5 y subir LERP a 0.22 — los pocos frames se sienten "saltones" si el lerp es muy bajo.

---

## Checklist al implementar

1. ✅ Re-encodar `hero-scrub.mp4` y `hero-scrub-mobile.mp4` con `keyint=1`
2. ✅ Extraer `hero-poster.jpg` con ffmpeg (frame del segundo 1)
3. ✅ Insertar marca `<!-- SCROLL-VIDEO-SECTION -->` en HTML
4. ✅ Añadir `<div class="hero-poster-bg">` antes del `<video>`
5. ✅ CSS con video oculto + canvas + poster bg
6. ✅ JS: bypass móvil + canvas approach desktop
7. ✅ Probar en desktop con cache disabled — debe ir fluido desde el primer scrub
8. ✅ Probar en móvil — autoplay loop normal

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

El vídeo del hero está siempre ligado a la posición del scroll mediante un
loop `requestAnimationFrame` que interpola `video.currentTime` hacia el
target calculado por el scroll. La velocidad de la transición es proporcional
a la velocidad del scroll de forma natural (lerp adaptativo cuando el diff es grande).

## Por qué este enfoque

Tres alternativas y por qué esta gana **cuando el vídeo está encodado con keyframe-per-frame** (ver sección de encoding):

| Enfoque | Problema |
|---|---|
| `video.play()` con `playbackRate` variable | No sigue al scroll real, acumula desfase. Saltos en backward (requiere seek). Snap final al parar de scrollear → jolts visibles. |
| `currentTime` directo (sin lerp) | Si el scroll es rápido, salta de un frame a otro lejano → trompicones. Usuario ve teletransportes. |
| **`currentTime` con lerp + rAF (recomendado)** | El vídeo persigue el target del scroll suavemente. Sin saltos, sin snaps, sin playbackRate. Solo funciona bien con keyframe-per-frame, pero ahí es perfecto. |

> **Lección clave (validada con cliente real, 2026-04-26 en Motobiker Xperiences):** El approach híbrido `playbackRate + seek` produce saltos bruscos puntuales por sus tres jolts (catch-up seek, snap-on-stop, backward seeks). El rAF lerp continuo no tiene jolts. Con keyframe-per-frame ya en sitio, escribir `video.currentTime` cuesta casi cero — **siempre preferir rAF lerp**.

---

## 1. Encoding correcto (no negociable)

**Sin keyframe-per-frame, ningún approach es fluido.** Re-encodar SIEMPRE los vídeos antes de servirlos:

```bash
# Desktop (1920x1080 o lo que sea el original, mantener resolución)
ffmpeg -i hero.mp4 \
  -c:v libx264 -x264opts "keyint=1:min-keyint=1:no-scenecut" \
  -crf 23 -preset slow -tune film \
  -an -movflags +faststart \
  -y hero-scrub.mp4

# Mobile (escalar a 1280px ancho para reducir peso)
ffmpeg -i hero.mp4 \
  -c:v libx264 -x264opts "keyint=1:min-keyint=1:no-scenecut" \
  -crf 24 -preset slow -tune film \
  -vf "scale=1280:-2" -an -movflags +faststart \
  -y hero-scrub-mobile.mp4
```

**Por qué keyint=1:** cada frame del vídeo es un keyframe independiente. Cualquier `video.currentTime = X` se decodifica al instante (no hay que rebobinar al keyframe anterior). Sin esto, los seeks tardan decenas de ms y se ven los trompicones.

**Coste:** archivos un 5-15% más grandes que con encoding por defecto. Vale la pena.

**Extraer poster:**
```bash
ffmpeg -ss 00:00:02 -i hero-scrub.mp4 -frames:v 1 -q:v 2 hero-poster.jpg
```

---

## 2. Estructura HTML

```html
<!-- SCROLL-VIDEO-SECTION -->
<div class="scroll-video-wrapper">
  <section class="hero">
    <video id="heroVideo" muted playsinline preload="auto" poster="assets/hero-poster.jpg">
      <source src="assets/hero-scrub-mobile.mp4" type="video/mp4" media="(max-width: 768px)">
      <source src="assets/hero-scrub.mp4" type="video/mp4">
    </video>
    <!-- resto del hero -->
  </section>
</div>
```

Sin `autoplay` ni `loop` en el HTML — el JS los activa solo en móvil.

---

## 3. CSS

```css
.scroll-video-wrapper { height: 175vh; }
.scroll-video-wrapper .hero { position: sticky; top: 0; height: 100vh; }

/* Móvil: hero normal sin scroll-driven (Safari iOS no soporta scrubbing fiable) */
@media (max-width: 768px) {
  .scroll-video-wrapper { height: auto; }
  .scroll-video-wrapper .hero { position: relative; }
}

/* IMPORTANTE — Si tu base CSS tiene un `.hero-placeholder` con background visible
   (gradient, color, etc.), ocúltalo. Sino tapa el <video>: */
.hero-placeholder { display: none; }
```

---

## 4. JS completo (rAF lerp continuo — recomendado)

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

// DESKTOP: rAF lerp continuo
// Con keyframe-per-frame, asignar currentTime cuesta casi nada → podemos
// interpolar suavemente hacia el target en cada frame sin saltos ni snaps.
(function () {
  if (window.matchMedia('(max-width: 768px)').matches) return;

  var video   = document.getElementById('heroVideo');
  var wrapper = document.querySelector('.scroll-video-wrapper');
  if (!video || !wrapper) return;

  var complete = false;
  var rafId    = null;
  var current  = 0;
  var LERP     = 0.18; // 0.10 muy cinematográfico · 0.18 balanceado · 0.30 muy reactivo

  function wrapTop() { return wrapper.getBoundingClientRect().top + window.scrollY; }
  function range()   { return Math.max(1, wrapper.offsetHeight - window.innerHeight); }
  function targetTime() {
    if (!video.duration) return 0;
    var scrolled = Math.max(0, window.scrollY - wrapTop());
    return Math.min(1, scrolled / range()) * video.duration;
  }

  function tick() {
    if (!video.duration) { rafId = null; return; }
    var target = targetTime();
    var diff   = target - current;
    // Lerp adaptativo: si scroll muy rápido (diff > 0.8s), aceleramos
    var k = Math.abs(diff) > 0.8 ? Math.min(0.5, LERP + Math.abs(diff) * 0.08) : LERP;
    if (Math.abs(diff) < 0.003) {
      current = target;
      try { video.currentTime = current; } catch (_) {}
      if (target >= video.duration - 0.1) complete = true;
      rafId = null;
      return;
    }
    current += diff * k;
    try { video.currentTime = current; } catch (_) {}
    rafId = requestAnimationFrame(tick);
  }

  function onScroll() {
    if (!video.duration) return;
    if (!rafId) rafId = requestAnimationFrame(tick);
  }

  // Bloquear scroll desktop hasta que el vídeo termine
  window.addEventListener('wheel', function (e) {
    if (complete || !video.duration || e.deltaY <= 0) return;
    var wrapperEnd = wrapTop() + range();
    if (window.scrollY + e.deltaY > wrapperEnd && video.currentTime < video.duration - 0.3) {
      e.preventDefault();
    }
  }, { passive: false });

  // Bloquear scroll touch (sin esto en móvil el wrapper no se respeta)
  var touchStartY = 0;
  window.addEventListener('touchstart', function (e) {
    touchStartY = e.touches[0].clientY;
  }, { passive: true });
  window.addEventListener('touchmove', function (e) {
    if (complete || !video.duration) return;
    var dy = touchStartY - e.touches[0].clientY;
    if (dy <= 0) return;
    var wrapperEnd = wrapTop() + range();
    if (window.scrollY + dy > wrapperEnd && video.currentTime < video.duration - 0.3) {
      e.preventDefault();
    }
  }, { passive: false });

  window.addEventListener('scroll', onScroll, { passive: true });
  video.addEventListener('loadeddata', function () {
    video.pause();
    current = 0;
    video.currentTime = 0;
    onScroll();
  });
  video.addEventListener('ended', function () { complete = true; });
}());
```

---

## Ajustes

| Qué | Dónde | Efecto |
|---|---|---|
| Reactividad del lerp | `var LERP = 0.18` | 0.10 = muy cinematográfico (vídeo va con delay). 0.30 = muy reactivo. 0.50+ = casi sin lerp. |
| Umbral del lerp adaptativo | `Math.abs(diff) > 0.8` | Si subes a 1.5, sólo acelera con scroll muy rápido (más cinematográfico). |
| Cap del lerp adaptativo | `Math.min(0.5, ...)` | Cuánto puede subir como máximo. |
| Duración del scroll | `175vh` en CSS | Menos = transición más corta. Más = más espacio para "vivir" el vídeo. |
| Tolerancia de bloqueo | `0.3` segundos | Margen antes del final para considerar "completo". |
| Threshold de parada del rAF | `Math.abs(diff) < 0.003` | Cuándo detener el loop. Bajar si percibes vibración; subir si percibes parada brusca. |

---

## Approach alternativo (sólo si NO puedes re-encodar)

Si por alguna razón no tienes acceso a re-encodar el vídeo, usa el **approach híbrido playbackRate + seek**. Tiene jolts puntuales pero funciona aceptablemente con encoding normal:

```javascript
// Solo si NO puedes re-encodar. Tiene jolts visibles.
// (Forward: playbackRate proporcional al diff. Backward: seeks throttleados. Snap al parar.)
(function () {
  if (window.matchMedia('(max-width: 768px)').matches) return;
  var video   = document.getElementById('heroVideo');
  var wrapper = document.querySelector('.scroll-video-wrapper');
  if (!video || !wrapper) return;

  var complete = false, lastY = window.scrollY, lastSeek = 0, stopT = null;
  function wrapTop() { return wrapper.getBoundingClientRect().top + window.scrollY; }
  function range()   { return wrapper.offsetHeight - window.innerHeight; }
  function targetTime() {
    if (!video.duration) return 0;
    var s = Math.max(0, window.scrollY - wrapTop());
    return Math.min(1, s / range()) * video.duration;
  }
  function onScroll() {
    if (!video.duration) return;
    var dy = window.scrollY - lastY; lastY = window.scrollY;
    if (dy === 0) return;
    clearTimeout(stopT);
    var t = targetTime(), c = video.currentTime, diff = t - c, now = performance.now();
    if (dy > 0) {
      if (diff > 2 && now - lastSeek > 250) { video.currentTime = t - 0.5; lastSeek = now; }
      video.playbackRate = Math.max(1, Math.min(8, 1 + Math.max(0, diff) * 1.5));
      if (video.paused) video.play().catch(function(){});
    } else {
      if (now - lastSeek > 80) { video.pause(); video.currentTime = t; lastSeek = now; }
    }
    stopT = setTimeout(function () {
      video.pause(); video.currentTime = targetTime();
      if (video.duration && video.currentTime >= video.duration - 0.2) complete = true;
    }, 150);
  }
  // (wheel/touch blocking igual que en el rAF lerp)
  window.addEventListener('scroll', onScroll, { passive: true });
}());
```

**Cuándo usarlo:** sólo si tienes acceso al vídeo final ya servido y no puedes pasarlo por ffmpeg.
**Cuándo NO:** prácticamente nunca — re-encodar lleva 30s y elimina el problema de raíz.

---

## Checklist al implementar

1. ✅ Re-encodar `hero.mp4` → `hero-scrub.mp4` con `keyint=1` (sección 1)
2. ✅ Re-encodar versión móvil escalada a 1280px
3. ✅ Extraer `hero-poster.jpg` con ffmpeg
4. ✅ Insertar marca `<!-- SCROLL-VIDEO-SECTION -->` en HTML
5. ✅ HTML con `.scroll-video-wrapper` + `.hero` con `<video>` (sin autoplay/loop)
6. ✅ CSS con `height: 175vh` + `position: sticky`
7. ✅ Verificar que `.hero-placeholder` esté `display: none` si existe en el CSS base
8. ✅ JS: bypass móvil + rAF lerp desktop
9. ✅ Probar en desktop: scroll fluido sin jolts, bloqueo al final hasta acabar
10. ✅ Probar en móvil: autoplay loop, scroll continúa normal

---

## Notas

- **Si el vídeo va a trompicones en general** (no específicos al scroll), es por el encoding. Re-encodar con `keyint=1` (sección 1).
- **Si en móvil va a tirones**: el touchmove bloquea correctamente, pero móviles antiguos pueden no decodificar 1080p suavemente — escala a 1280px o 960px.
- **Tamaño esperado:** un vídeo de 5s @ 24fps a 1080p con keyframe-per-frame pesa 8-10MB. A 1280px, 3-5MB. Es lo normal.
- El bloqueo del wheel solo actúa al **final del wrapper**, no dentro de él, para evitar deadlocks (el vídeo necesita scroll para avanzar).
- **Ojo con `.hero-placeholder` visible:** si tu base CSS tiene un placeholder absolute con gradient, tapará el `<video>`. Forzar `display: none` en CSS.

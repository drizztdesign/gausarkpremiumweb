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
a la velocidad del scroll de forma natural (más diff → más avance por frame).

## Por qué este enfoque

Tres alternativas y por qué esta gana:

| Enfoque | Problema |
|---|---|
| `video.play()` con `playbackRate` | Desconectado del scroll → puede saltar del inicio al final |
| `currentTime` directo (sin lerp) | Si el scroll es rápido, salta de un frame a otro lejano → trompicones |
| **`currentTime` con lerp + rAF** | El vídeo siempre persigue la posición del scroll suavemente |

Como bonus, el lerp da automáticamente velocidad proporcional al scroll: si
el target está lejos (scroll rápido), `diff * 0.22` es grande y el vídeo
avanza rápido. Si el target está cerca (scroll lento), avanza suave.

---

## Estructura HTML

```html
<!-- SCROLL-VIDEO-SECTION -->
<div class="scroll-video-wrapper">
  <section class="hero">
    <video id="heroVideo" muted playsinline preload="auto">
      <!-- Móvil: 720p liviano (~5MB) -->
      <source src="assets/hero-scrub-mobile.mp4" type="video/mp4" media="(max-width: 768px)">
      <!-- Desktop: full quality -->
      <source src="assets/hero-scrub.mp4" type="video/mp4">
    </video>
    <!-- resto del hero -->
  </section>
</div>
```

Sin `autoplay` ni `loop`.

**Generar la versión móvil con FFmpeg:**
```bash
ffmpeg -i hero.mp4 \
  -c:v libx264 -x264opts "keyint=1:min-keyint=1:no-scenecut" \
  -crf 22 -preset slow -tune film \
  -vf "scale=1280:-2" -an -movflags +faststart \
  -y hero-scrub-mobile.mp4
```

---

## CSS

```css
.scroll-video-wrapper { height: 175vh; }
.scroll-video-wrapper .hero { position: sticky; top: 0; height: 100vh; }

/* Móvil: hero normal sin scroll-driven (Safari iOS no soporta scrubbing fiable) */
@media (max-width: 768px) {
  .scroll-video-wrapper { height: auto; }
  .scroll-video-wrapper .hero { position: relative; }
}
```

---

## JS completo

```javascript
// MÓVIL: bypass scroll-driven (usar autoplay simple, siempre fluido)
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

// DESKTOP: scroll-driven scrubbing
(function () {
  if (window.matchMedia('(max-width: 768px)').matches) return;

  var video   = document.getElementById('heroVideo');
  var wrapper = document.querySelector('.scroll-video-wrapper');
  if (!video || !wrapper) return;

  var complete     = false;
  var lastY        = window.scrollY;
  var lastSeekTime = 0;
  var stopTimer    = null;

  function wrapTop() { return wrapper.getBoundingClientRect().top + window.scrollY; }
  function range()   { return wrapper.offsetHeight - window.innerHeight; }

  function targetTime() {
    if (!video.duration) return 0;
    var scrolled = Math.max(0, window.scrollY - wrapTop());
    return Math.min(1, scrolled / range()) * video.duration;
  }

  // Estrategia híbrida: play() con playbackRate dinámico, sin seeks por frame
  function onScroll() {
    if (!video.duration) return;
    var dy = window.scrollY - lastY;
    lastY = window.scrollY;
    if (dy === 0) return;

    clearTimeout(stopTimer);

    var target  = targetTime();
    var current = video.currentTime;
    var diff    = target - current;
    var now     = performance.now();

    if (dy > 0) {
      // Forward: playbackRate proporcional al diff
      if (diff > 2 && now - lastSeekTime > 250) {
        video.currentTime = target - 0.5;
        lastSeekTime = now;
      }
      var rate = Math.max(1, Math.min(8, 1 + Math.max(0, diff) * 1.5));
      video.playbackRate = rate;
      if (video.paused) video.play().catch(function () {});
    } else {
      // Backward: seek throttleado
      if (now - lastSeekTime > 80) {
        video.pause();
        video.currentTime = target;
        lastSeekTime = now;
      }
    }

    stopTimer = setTimeout(function () {
      video.pause();
      video.currentTime = targetTime();
      if (video.duration && video.currentTime >= video.duration - 0.2) complete = true;
    }, 150);
  }

  // Bloquear scroll desktop (wheel) si el vídeo no ha terminado
  window.addEventListener('wheel', function (e) {
    if (complete || !video.duration || e.deltaY <= 0) return;
    var wrapperEnd = wrapTop() + range();
    if (window.scrollY + e.deltaY > wrapperEnd && video.currentTime < video.duration - 0.3) {
      e.preventDefault();
    }
  }, { passive: false });

  // Bloquear scroll móvil (touch) — sin esto, en móvil el wrapper no se respeta
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
    video.currentTime = 0;
  });
  video.addEventListener('ended', function () { complete = true; });
}());
```

---

## Ajustes

| Qué | Dónde | Efecto |
|---|---|---|
| Reactividad del lerp | `diff * 0.22` | Más alto (0.35) = más reactivo. Más bajo (0.10) = más cinematográfico |
| Duración del scroll | `175vh` en CSS | Menos = transición más corta |
| Tolerancia de bloqueo | `0.3` segundos | Margen antes del final para considerar "completo" |

## Notas

- Si el vídeo va a trompicones en general (no específicos al scroll), es por
  el encoding del archivo. Re-encodar con keyframes en cada frame:
  `ffmpeg -i input.mp4 -c:v libx264 -x264opts "keyint=1:min-keyint=1" -crf 30 -preset ultrafast output.mp4`
- El bloqueo del wheel solo actúa al **final del wrapper**, no dentro de él,
  para evitar deadlocks (el vídeo necesita scroll para avanzar).

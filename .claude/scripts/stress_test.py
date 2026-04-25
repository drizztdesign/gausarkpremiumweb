"""Simulate fast wheel scroll to measure FPS during scrubbing."""
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto("http://localhost:8767/index.html", wait_until="domcontentloaded")
        await page.wait_for_function("document.getElementById('heroVideo').readyState >= 2", timeout=15000)
        await asyncio.sleep(2)

        # Inject FPS counter
        await page.evaluate("""
          window._frames = 0;
          window._start = performance.now();
          (function loop() {
            window._frames++;
            requestAnimationFrame(loop);
          })();
        """)

        # Reset counters
        await page.evaluate("window._frames = 0; window._start = performance.now();")

        # Simulate fast scroll: 50 wheel events of 30px each over 1 second
        for i in range(50):
            await page.mouse.wheel(0, 30)
            await asyncio.sleep(0.02)

        await asyncio.sleep(1.5)  # let it settle

        result = await page.evaluate("""() => {
          const elapsed = performance.now() - window._start;
          const fps = (window._frames / elapsed) * 1000;
          const v = document.getElementById('heroVideo');
          return { fps: fps.toFixed(1), elapsed: elapsed.toFixed(0), scrollY: window.scrollY,
                   videoTime: v.currentTime.toFixed(2), videoDuration: v.duration };
        }""")
        print("STRESS TEST RESULT:")
        for k, v in result.items():
            print(f"  {k}: {v}")

        await browser.close()


asyncio.run(main())

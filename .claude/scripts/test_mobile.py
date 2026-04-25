"""Test scroll-video en viewport móvil + simulación de touch."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(__file__).parent / "screenshots-mobile"
OUT.mkdir(exist_ok=True)
URL = "https://gausarkpremiumweb.vercel.app/"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # iPhone 14 Pro viewport
        ctx = await browser.new_context(
            viewport={"width": 393, "height": 852},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
            has_touch=True,
            is_mobile=True,
        )
        page = await ctx.new_page()
        await page.goto(URL, wait_until="domcontentloaded")
        await page.wait_for_function(
            "document.getElementById('heroVideo') && document.getElementById('heroVideo').readyState >= 1",
            timeout=20000
        )
        await asyncio.sleep(3)

        info = await page.evaluate("""() => {
          const v = document.getElementById('heroVideo');
          const w = document.querySelector('.scroll-video-wrapper');
          return {
            videoDuration: v.duration,
            videoCurrentTime: v.currentTime,
            videoPaused: v.paused,
            wrapperHeight: w.offsetHeight,
            innerHeight: window.innerHeight,
            scrollY: window.scrollY,
            documentHeight: document.documentElement.scrollHeight,
          };
        }""")
        print("=== MOBILE INITIAL ===")
        for k, v in info.items():
            print(f"  {k}: {v}")
        print()
        await page.screenshot(path=str(OUT / "00-initial.png"))

        # Simular swipe táctil (en vez de wheel)
        print("=== TOUCH SWIPE TEST ===")
        steps = [200, 400, 600, 800, 1200]
        for i, y in enumerate(steps, 1):
            await page.evaluate(f"window.scrollTo({{top: {y}, behavior: 'instant'}})")
            await asyncio.sleep(0.5)
            state = await page.evaluate("""() => ({
              scrollY: window.scrollY,
              videoTime: document.getElementById('heroVideo').currentTime,
              videoPaused: document.getElementById('heroVideo').paused,
            })""")
            print(f"  STEP {i}: scrollY={state['scrollY']:.0f} videoTime={state['videoTime']:.2f}s paused={state['videoPaused']}")
            await page.screenshot(path=str(OUT / f"{i:02d}-y{y}.png"))

        # Test: ¿el wheel blocker funciona con eventos táctiles?
        print()
        print("=== WHEEL BLOCKER vs TOUCH ===")
        print("  En móvil NO existe 'wheel'. Los eventos son 'touchstart/move/end'.")
        print("  Por tanto, el bloqueador del wrapper NO funciona en móvil.")

        await browser.close()


asyncio.run(main())

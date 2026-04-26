 """Test scroll-driven video. Scrolls in steps, captures screenshots, measures lag."""
import asyncio
import time
from pathlib import Path
from playwright.async_api import async_playwright

OUT = Path(__file__).parent / "screenshots"
OUT.mkdir(exist_ok=True)
URL = "http://localhost:8767/index.html"


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await ctx.new_page()

        console_logs = []
        page.on("console", lambda m: console_logs.append(f"[{m.type}] {m.text}"))
        page.on("pageerror", lambda e: console_logs.append(f"[error] {e}"))

        await page.goto(URL, wait_until="domcontentloaded")
        await page.wait_for_function("document.getElementById('heroVideo') && document.getElementById('heroVideo').readyState >= 1", timeout=30000)
        await asyncio.sleep(2)  # let video load some data

        # Initial state
        info = await page.evaluate("""() => {
          const v = document.getElementById('heroVideo');
          const w = document.querySelector('.scroll-video-wrapper');
          return {
            videoDuration: v.duration,
            videoCurrentTime: v.currentTime,
            videoReadyState: v.readyState,
            videoPaused: v.paused,
            wrapperHeight: w.offsetHeight,
            windowInnerHeight: window.innerHeight,
            scrollY: window.scrollY,
            documentHeight: document.documentElement.scrollHeight,
          };
        }""")
        print("INITIAL STATE:")
        for k, v in info.items():
            print(f"  {k}: {v}")
        print()

        await page.screenshot(path=str(OUT / "00-initial.png"))

        # Scroll progressively and measure
        steps = [100, 250, 400, 600, 800, 1000]
        results = []
        for i, y in enumerate(steps, 1):
            # Animate scroll + force-fire scroll event
            await page.evaluate(f"""
              window.scrollTo({{top: {y}, behavior: 'instant'}});
              window.dispatchEvent(new Event('scroll'));
            """)
            await asyncio.sleep(0.5)  # wait for rAF + throttle
            state = await page.evaluate("""() => ({
              scrollY: window.scrollY,
              videoCurrentTime: document.getElementById('heroVideo').currentTime,
              videoPaused: document.getElementById('heroVideo').paused,
              videoPlaybackRate: document.getElementById('heroVideo').playbackRate,
            })""")
            results.append({"step": i, "scrollY_target": y, **state})
            print(f"STEP {i}: scrollY={state['scrollY']:.0f} videoTime={state['videoCurrentTime']:.2f}s paused={state['videoPaused']} rate={state['videoPlaybackRate']}")
            await page.screenshot(path=str(OUT / f"{i:02d}-scroll-{y}.png"))

        # Try scrolling further (should be blocked if video not done)
        print("\n--- Try scrolling beyond wrapper ---")
        await page.evaluate("window.scrollTo({top: 2000, behavior: 'instant'})")
        await asyncio.sleep(0.5)
        state = await page.evaluate("""() => ({
          scrollY: window.scrollY,
          videoCurrentTime: document.getElementById('heroVideo').currentTime,
          videoDuration: document.getElementById('heroVideo').duration,
        })""")
        print(f"After scrollTo(2000): scrollY={state['scrollY']:.0f} videoTime={state['videoCurrentTime']:.2f}/{state['videoDuration']:.2f}")
        await page.screenshot(path=str(OUT / "99-end.png"))

        # Scroll back
        print("\n--- Scroll back to 0 ---")
        await page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
        await asyncio.sleep(0.5)
        state = await page.evaluate("""() => ({
          scrollY: window.scrollY,
          videoCurrentTime: document.getElementById('heroVideo').currentTime,
        })""")
        print(f"After scrollTo(0): scrollY={state['scrollY']:.0f} videoTime={state['videoCurrentTime']:.2f}")
        await page.screenshot(path=str(OUT / "ZZ-back.png"))

        if console_logs:
            print("\n--- CONSOLE ---")
            for log in console_logs:
                print(log)

        await browser.close()


asyncio.run(main())

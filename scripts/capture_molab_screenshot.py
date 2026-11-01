import marimo._code_mode as cm

async def capture():
    async with cm.get_context(skip_staleness_check=True) as ctx:
        print("Capturing screenshot of vblA...")
        await ctx.screenshot(target="vblA", save_to="/marimo/molab_ui_streamlined.png")
        print("Screenshot saved to /marimo/molab_ui_streamlined.png")

await capture()

#!/usr/bin/env python3
"""
Renders the README screenshots from preview/demo.html with the real built stylesheet.

  cd preview && npm install      # local webfonts (once)
  python3 scripts/build.py
  python3 scripts/render_previews.py

Requires: pip install playwright pillow && python3 -m playwright install chromium
"""
import functools
import http.server
import threading
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "previews"
THEMES = [("shirokuro", "dark"), ("washi", "light"), ("sakura", "light"), ("neon", "dark"), ("game", "light")]
EXTRA = [("shirokuro", "light"), ("washi", "dark"), ("sakura", "dark")]


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(Quiet, directory=str(ROOT))
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, httpd.server_address[1]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    httpd, port = serve()
    base = f"http://127.0.0.1:{port}/preview/demo.html"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        ctx.route("**/fonts.googleapis.com/**", lambda r: r.abort())
        page = ctx.new_page()

        def shot(theme, mode, view, name):
            page.goto(f"{base}?theme={theme}&mode={mode}&view={view}")
            page.wait_for_function("document.getElementById('douga-style') && document.fonts.status === 'loaded'")
            page.wait_for_timeout(400)
            page.screenshot(path=str(OUT / name))
            print("✓", name)

        for theme, mode in THEMES:
            shot(theme, mode, "home", f"{theme}-home.png")
            shot(theme, mode, "watch", f"{theme}-watch.png")
        for theme, mode in EXTRA:
            shot(theme, mode, "home", f"{theme}-home-{mode}.png")

        # theme-switch toast
        page.goto(f"{base}?theme=shirokuro&mode=dark&view=home")
        page.wait_for_function("document.getElementById('douga-style') && document.fonts.status === 'loaded'")
        page.keyboard.press("Alt+Shift+KeyT")
        page.wait_for_timeout(450)
        page.screenshot(path=str(OUT / "switch-toast.png"), clip={"x": 420, "y": 640, "width": 600, "height": 260})
        print("✓ switch-toast.png")
        browser.close()
    httpd.shutdown()

    # banner: five diagonal-free vertical slices of the home screens
    slices = [Image.open(OUT / f"{t}-home.png").crop((60, 0, 60 + 1440, 900)) for t, _ in THEMES]
    w = 1440 // len(slices)
    banner = Image.new("RGB", (1440, 900))
    for i, img in enumerate(slices):
        banner.paste(img.crop((i * w, 0, (i + 1) * w, 900)), (i * w, 0))
    d = ImageDraw.Draw(banner)
    for i in range(1, len(slices)):
        d.line([(i * w, 0), (i * w, 900)], fill="#000000", width=4)
    banner.resize((1440, 900)).save(OUT / "banner.png")
    print("✓ banner.png")


if __name__ == "__main__":
    main()

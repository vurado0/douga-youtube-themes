#!/usr/bin/env python3
"""
DOUGA build — turns src/ into everything people install.

  python3 scripts/build.py

Outputs (dist/):
  extension/                   unpacked WebExtension (Chrome, Arc, Edge, Brave, Firefox, Safari converter)
  douga-extension-vX.Y.Z.zip   the same, zipped for releases
  douga.user.js                userscript (Safari "Userscripts", Tampermonkey, Violentmonkey)
  stylus/douga-<theme>.user.css  one standalone UserCSS per theme (Stylus)
Requires: Python 3.9+ and Pillow (pip install pillow) for the icons.
"""
import json
import re
import shutil
import urllib.parse
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
VERSION = (ROOT / "VERSION").read_text().strip()
REPO = "vurado0/douga-youtube-themes"
DEFAULT_THEME = "shirokuro"
FONTS = (
    "https://fonts.googleapis.com/css2"
    "?family=DotGothic16"
    "&family=M+PLUS+Rounded+1c:wght@400;500;700;800"
    "&family=Zen+Maru+Gothic:wght@700;900"
    "&family=Shippori+Mincho:wght@500;700"
    "&family=Noto+Sans+JP:wght@400;500;700"
    "&family=Mochiy+Pop+One"
    "&family=Zen+Kaku+Gothic+New:wght@400;700;900"
    "&display=swap"
)


def svg_data_uri(name: str) -> str:
    svg = (SRC / "logos" / name).read_text().strip()
    svg = re.sub(r">\s+<", "><", svg)
    return "data:image/svg+xml," + urllib.parse.quote(svg, safe=" /=:'")


def load_themes():
    themes = {}
    for path in sorted((SRC / "themes").glob("*.css")):
        raw = path.read_text()
        meta = {k: v.strip() for k, v in re.findall(r"@(\w+)[ \t]+(.+)", raw.split("*/", 1)[0])}
        css = raw.split("*/", 1)[1].strip()
        css = re.sub(r"\{\{logo:([\w.-]+)\}\}", lambda m: svg_data_uri(m.group(1)), css)
        for key in ("id", "vol", "name", "jp", "tagline", "swatches"):
            assert key in meta, f"{path.name}: missing @{key}"
        themes[meta["id"]] = {
            "id": meta["id"],
            "vol": meta["vol"],
            "name": meta["name"],
            "jp": meta["jp"],
            "tagline": meta["tagline"],
            "swatches": [s.strip() for s in meta["swatches"].split(",")],
            "css": css,
        }
    assert DEFAULT_THEME in themes
    return themes


def check_css(name: str, css: str):
    depth = 0
    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    for ch in re.sub(r'"[^"]*"|\'[^\']*\'', "", stripped):
        depth += ch == "{"
        depth -= ch == "}"
        assert depth >= 0, f"{name}: unbalanced braces"
    assert depth == 0, f"{name}: unbalanced braces"


def make_icons(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    size = 1024
    k = size / 40
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([2 * k, 4 * k, 38 * k, 36 * k], radius=12 * k, fill="#0A0A0A")
    for cx in (14, 26):
        d.ellipse([(cx - 2.6) * k, 16.4 * k, (cx + 2.6) * k, 21.6 * k], fill="white")
    w = int(1.0 * k)
    d.arc([16.3 * k, 23.6 * k, 20.0 * k, 27.0 * k], 0, 180, fill="white", width=w)
    d.arc([20.0 * k, 23.6 * k, 23.7 * k, 27.0 * k], 0, 180, fill="white", width=w)
    star = [(33, 1), (34.2, 4.3), (37.5, 5.5), (34.2, 6.7), (33, 10), (31.8, 6.7), (28.5, 5.5), (31.8, 4.3)]
    d.polygon([(x * k, y * k) for x, y in star], fill="#0A0A0A", outline="white", width=int(k * 0.6))
    for s in (16, 32, 48, 128):
        img.resize((s, s), Image.LANCZOS).save(out / f"icon{s}.png")
    return img


def main():
    shutil.rmtree(DIST, ignore_errors=True)
    ext = DIST / "extension"
    (ext / "popup").mkdir(parents=True)

    base = (SRC / "base.css").read_text()
    check_css("base.css", base)
    themes = load_themes()
    for t in themes.values():
        check_css(t["id"], t["css"])

    # ── content script (shared by extension + userscript) ──
    content = (SRC / "content.template.js").read_text()
    replacements = {
        "__VERSION__": VERSION,
        "__REPO__": REPO,
        "'__DEFAULT__'": json.dumps(DEFAULT_THEME),
        "'__FONTS__'": json.dumps(FONTS),
        "__BASE__": json.dumps(base, ensure_ascii=False),
        "__THEMES__": json.dumps(
            {k: {kk: v[kk] for kk in ("vol", "name", "jp", "css")} for k, v in themes.items()},
            ensure_ascii=False,
        ),
    }
    for key, value in replacements.items():
        assert key in content, key
        content = content.replace(key, value)

    # ── WebExtension ──
    icon = make_icons(ext / "icons")
    (ext / "content.js").write_text(content)
    manifest = {
        "manifest_version": 3,
        "name": "DOUGA どうが — Japanese Themes for YouTube",
        "short_name": "DOUGA",
        "version": VERSION,
        "description": "Five hand-made Japanese theme packs for YouTube — Shirokuro, Washi, Sakura Pop, Neon Yoichi and 8-Bit Pocket.",
        "homepage_url": f"https://github.com/{REPO}",
        "icons": {str(s): f"icons/icon{s}.png" for s in (16, 32, 48, 128)},
        "action": {
            "default_title": "DOUGA themes",
            "default_popup": "popup/popup.html",
            "default_icon": {str(s): f"icons/icon{s}.png" for s in (16, 32, 48)},
        },
        "permissions": ["storage"],
        "content_scripts": [
            {"matches": ["https://www.youtube.com/*"], "js": ["content.js"], "run_at": "document_start"}
        ],
        "browser_specific_settings": {
            "gecko": {"id": "douga-themes@vurado0.github.io", "strict_min_version": "109.0"}
        },
    }
    (ext / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    for f in ("popup.html", "popup.css", "popup.js"):
        shutil.copy(SRC / "popup" / f, ext / "popup" / f)
    meta = [{k: t[k] for k in ("id", "vol", "name", "jp", "tagline", "swatches")} for t in themes.values()]
    (ext / "popup" / "themes.js").write_text(
        "const DOUGA_THEMES = " + json.dumps(meta, ensure_ascii=False, indent=2) + ";\n"
    )

    zip_path = DIST / f"douga-extension-v{VERSION}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(ext.rglob("*")):
            if f.is_file():
                z.write(f, Path("douga-extension") / f.relative_to(ext))

    # ── Userscript ──
    header = f"""// ==UserScript==
// @name         DOUGA どうが — Japanese Themes for YouTube
// @namespace    https://github.com/{REPO}
// @version      {VERSION}
// @description  Five Japanese theme packs for YouTube. Alt/Option+Shift+T switches themes, Alt/Option+Shift+X turns the skin off.
// @author       vurado0
// @homepageURL  https://github.com/{REPO}
// @downloadURL  https://raw.githubusercontent.com/{REPO}/main/dist/douga.user.js
// @updateURL    https://raw.githubusercontent.com/{REPO}/main/dist/douga.user.js
// @match        https://www.youtube.com/*
// @run-at       document-start
// @inject-into  content
// @grant        none
// ==/UserScript==

"""
    (DIST / "douga.user.js").write_text(header + content)

    # ── Stylus: one UserCSS per theme ──
    stylus = DIST / "stylus"
    stylus.mkdir()
    for t in themes.values():
        (stylus / f"douga-{t['id']}.user.css").write_text(
            f"""/* ==UserStyle==
@name         DOUGA Vol.{t['vol']} {t['jp']} {t['name']} — YouTube
@namespace    https://github.com/{REPO}
@version      {VERSION}
@description  {t['tagline']}
@preprocessor default
==/UserStyle== */
@import url('{FONTS}');

@-moz-document domain("youtube.com") {{
{base}
{t['css']}
}}
"""
        )

    # brand icon for docs
    (ROOT / "assets").mkdir(exist_ok=True)
    icon.resize((512, 512), Image.LANCZOS).save(ROOT / "assets" / "douga-icon.png")

    for f in sorted(DIST.rglob("*")):
        if f.is_file():
            print(f"{f.relative_to(ROOT)}  {f.stat().st_size:,} B")


if __name__ == "__main__":
    main()

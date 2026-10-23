"""Generates abstract sample thumbnails + avatars for the demo page (no real video content)."""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)
random.seed(7)
PALETTES = [
    ("#1D3557", "#E63946", "#F1FAEE"), ("#2A9D8F", "#E9C46A", "#264653"), ("#FF6B6B", "#FFE66D", "#4ECDC4"),
    ("#3D348B", "#F7B801", "#F18701"), ("#0B132B", "#5BC0BE", "#FFFFFF"), ("#6A4C93", "#FFCA3A", "#8AC926"),
    ("#E76F51", "#F4A261", "#2A9D8F"), ("#111111", "#FF006E", "#3A86FF"),
]
W, H = 640, 360
for i, (bg, a, b) in enumerate(PALETTES):
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    kind = i % 4
    if kind == 0:   # rising sun stripes
        for r in range(420, 0, -40):
            d.ellipse([W * .62 - r, H * .9 - r, W * .62 + r, H * .9 + r], fill=a if (r // 40) % 2 else b)
    elif kind == 1:  # waves
        for row in range(9):
            y0 = 40 + row * 38
            pts = [(x, y0 + 14 * math.sin(x / 38 + row)) for x in range(0, W + 8, 8)]
            d.line(pts, fill=a if row % 2 else b, width=12)
    elif kind == 2:  # confetti blocks
        for _ in range(26):
            x, y, s = random.randint(-20, W), random.randint(-20, H), random.randint(30, 110)
            d.rounded_rectangle([x, y, x + s, y + s * .7], radius=14, fill=random.choice((a, b)))
    else:            # mountain + moon
        d.polygon([(0, H), (W * .35, H * .3), (W * .6, H * .75), (W * .78, H * .45), (W, H)], fill=a)
        d.ellipse([W * .72, H * .1, W * .86, H * .35], fill=b)
    img = img.filter(ImageFilter.GaussianBlur(.6))
    img.save(OUT / f"thumb{i + 1}.jpg", quality=88)

AV = ["#FF8FB4", "#2BF5FF", "#F7B801", "#8AC926", "#B5452C", "#3A86FF"]
for i, c in enumerate(AV):
    img = Image.new("RGB", (120, 120), c)
    d = ImageDraw.Draw(img)
    d.ellipse([34, 40, 50, 56], fill="#111")
    d.ellipse([70, 40, 86, 56], fill="#111")
    d.arc([42, 58, 78, 86], 20, 160, fill="#111", width=6)
    img.save(OUT / f"avatar{i + 1}.png")
print("assets ok")

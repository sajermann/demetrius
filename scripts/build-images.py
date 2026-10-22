"""Builds every image the page serves from the originals in source-images/.

Run from the project root after adding or replacing an original:

    python scripts/build-images.py

Needs Pillow (pip install pillow). Output goes to assets/images/ and is safe to delete
and rebuild: nothing in there is edited by hand.
"""

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-images"
OUT = ROOT / "assets" / "images"

# Thumbnails sit in a circle; each appliance is scaled to fit this share of the square
# (width, height) so its corners stay inside the circle.
APPLIANCES = {
    "tv": (0.74, 0.70),
    "washing-machine": (0.72, 0.76),
    "circuit-board": (0.70, 0.78),
    "microwave": (0.76, 0.70),
    "air-fryer": (0.70, 0.78),
    "toaster-oven": (0.76, 0.70),
    "cooktop": (0.78, 0.70),
    "blender": (0.66, 0.80),
    "coffee-maker": (0.66, 0.80),
    "vacuum-cleaner": (0.78, 0.72),
}
THUMB_SIZES = (96, 192)          # shown at 72–88px: 1x and 2x screens
LARGE_BOXES = (400, 800)         # shown at up to 600px: phones/1x and 2x screens
CHARACTER_WIDTHS = (360, 540, 720, 980)
PHOTO_WIDTHS = (400, 800)

manifest = {}


def open_trimmed(path):
    """Opens an image and crops away its transparent margin."""
    im = Image.open(path).convert("RGBA")
    box = im.getchannel("A").point(lambda v: 255 if v > 16 else 0).getbbox()
    return im.crop(box) if box else im


def find_source(folder, name):
    matches = sorted(folder.glob(f"{name}.*"))
    if not matches:
        raise SystemExit(f"Missing original: {folder / name}.*")
    return matches[0]


def save_webp(im, path, quality=85):
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "WEBP", quality=quality, method=6)
    manifest[path.relative_to(ROOT).as_posix()] = list(im.size)


def build_appliances():
    for name, (fill_w, fill_h) in APPLIANCES.items():
        im = open_trimmed(find_source(SRC / "appliances", name))
        for size in THUMB_SIZES:
            obj = im.copy()
            obj.thumbnail((int(size * fill_w), int(size * fill_h)), Image.LANCZOS)
            canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            canvas.paste(obj, ((size - obj.width) // 2, (size - obj.height) // 2), obj)
            save_webp(canvas, OUT / "appliances" / "thumb" / f"{name}-{size}.webp", 88)
        for box in LARGE_BOXES:
            obj = im.copy()
            obj.thumbnail((box, box), Image.LANCZOS)  # never enlarges a small original
            save_webp(obj, OUT / "appliances" / "large" / f"{name}-{box}.webp")


def build_character():
    im = open_trimmed(find_source(SRC, "character"))
    for width in CHARACTER_WIDTHS:
        obj = im.copy()
        obj.thumbnail((width, 10_000), Image.LANCZOS)
        save_webp(obj, OUT / "character" / f"character-{width}.webp", 86)
    # Link previews (WhatsApp, Facebook) need a 1200x630 JPEG.
    og = Image.new("RGB", (1200, 630), (26, 86, 219))
    fig = im.copy()
    fig.thumbnail((10_000, 600), Image.LANCZOS)
    og.paste(fig, (1200 - fig.width - 120, 630 - fig.height), fig)
    og.save(OUT / "og-image.jpg", "JPEG", quality=85)
    manifest[(OUT / "og-image.jpg").relative_to(ROOT).as_posix()] = [1200, 630]


def build_photos():
    for path in sorted((SRC / "photos").glob("*.*")):
        im = Image.open(path).convert("RGB")
        for width in PHOTO_WIDTHS:
            obj = im.copy()
            obj.thumbnail((width, 10_000), Image.LANCZOS)
            save_webp(obj, OUT / "photos" / f"{path.stem}-{width}.webp", 82)


def build_logo():
    logo_path = SRC / "logo.png"
    if logo_path.exists():
        im = open_trimmed(logo_path)
        for size in (44, 88):
            obj = im.copy()
            obj.thumbnail((size, size), Image.LANCZOS)
            canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            canvas.paste(obj, ((size - obj.width) // 2, (size - obj.height) // 2), obj)
            name = "logo.webp" if size == 44 else f"logo-{size}.webp"
            save_webp(canvas, OUT / name, 92)

        # Favicons: PNG, multi-resolution ICO, and Apple touch icon
        icons_dir = ROOT / "assets" / "icons"
        icons_dir.mkdir(parents=True, exist_ok=True)
        fav = im.copy()
        fav.thumbnail((32, 32), Image.LANCZOS)
        c32 = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
        c32.paste(fav, ((32 - fav.width) // 2, (32 - fav.height) // 2), fav)
        c32.save(icons_dir / "favicon.png", "PNG")
        im.save(icons_dir / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])

        touch = im.copy()
        touch.thumbnail((180, 180), Image.LANCZOS)
        c180 = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
        c180.paste(touch, ((180 - touch.width) // 2, (180 - touch.height) // 2), touch)
        c180.save(icons_dir / "apple-touch-icon.png", "PNG")


if __name__ == "__main__":
    build_appliances()
    build_character()
    build_photos()
    build_logo()
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    for file, (w, h) in manifest.items():
        print(f"{w:>5} x {h:<5} {file}")

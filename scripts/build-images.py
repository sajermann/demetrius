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
    "refrigerator": (0.66, 0.80),
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


if __name__ == "__main__":
    build_appliances()
    build_character()
    build_photos()
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    for file, (w, h) in manifest.items():
        print(f"{w:>5} x {h:<5} {file}")

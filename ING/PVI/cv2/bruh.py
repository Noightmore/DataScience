import os
from typing import Dict, Tuple, List
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

IN_PATH  = "cv02_01.bmp"
OUT_PATH = "cv02_01_labeled.png"

def try_load_comic_sans(size: int) -> ImageFont.FreeTypeFont:
    possible = [
        "/Library/Fonts/Comic Sans MS.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/Comic_Sans_MS.ttf",
        "/usr/share/fonts/truetype/msttcorefonts/comic.ttf",
    ]
    for p in possible:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                pass
    # fallback
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=size)
    except Exception:
        return ImageFont.load_default()


def draw_centered_text(img_bgr: np.ndarray, text: str, center_xy: Tuple[int,int],
                       font: ImageFont.FreeTypeFont, fill=(0,0,0)) -> np.ndarray:

    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(rgb)
    d = ImageDraw.Draw(im)
    try:
        d.text(center_xy, text, font=font, fill=fill, anchor="mm")
    except TypeError:
        w = d.textlength(text, font=font)
        h = font.size
        d.text((center_xy[0]-w//2, center_xy[1]-h//2), text, font=font, fill=fill)
    return cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

def detect_color_name(bgr_pixel):
    """Return a text label for a single pixel given in BGR (OpenCV default)."""
    hsv = cv2.cvtColor(np.uint8([[bgr_pixel]]), cv2.COLOR_BGR2HSV)[0][0]
    h, s, v = hsv

    # --- Achromatic first ---
    if v <= 40:
        return "black"
    if s <= 30 and v >= 200:
        return "white"
    if s <= 40 < v < 200:
        return "gray"

    # --- Chromatic by hue ---
    if (h <= 8 or h >= 170) and s > 50 and v > 50:
        return "red"
    if 10 <= h <= 20:
        if v < 120:
            return "brown"
        return "orange"

    if 21 <= h <= 35:
        return "yellow"
    if 36 <= h <= 85:
        return "green"
    if 86 <= h <= 125:
        return "blue"
    if 126 <= h <= 155:
        return "purple"
    if 140 <= h <= 170 and v > 150:
        return "pink"
    # brown: darker orange
    if 9 <= h <= 24 and v < 150:
        return "brown"

    return "unknown"


def relative_luminance(bgr):
    # WCAG-ish luminance from sRGB (approx): Y = 0.2126 R + 0.7152 G + 0.0722 B
    b, g, r = [c/255.0 for c in bgr]
    return 0.2126*r + 0.7152*g + 0.0722*b

def main():
    # ---- SETTINGS ----
    TILE_W = 199
    TILE_H = 199
    OFF_X = 0
    OFF_Y = 0

    img = cv2.imread(IN_PATH, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"Cannot read {IN_PATH}")
    H, W = img.shape[:2]

    out  = img.copy()
    font = try_load_comic_sans(max(16, W // 35))

    y = OFF_Y
    while y + TILE_H <= H:
        x = OFF_X
        while x + TILE_W <= W:
            tile = img[y:y+TILE_H, x:x+TILE_W]

            # use inner area (80%) to avoid borders
            pad_x = max(1, int(TILE_W * 0.1))
            pad_y = max(1, int(TILE_H * 0.1))
            ix, iy = x + pad_x, y + pad_y
            iw, ih = TILE_W - 2*pad_x, TILE_H - 2*pad_y
            inner = img[iy:iy+ih, ix:ix+iw]

            avg_bgr = inner.reshape(-1, 3).mean(axis=0)

            name = detect_color_name(avg_bgr.astype(np.uint8).tolist())

            Y = relative_luminance(avg_bgr)
            text_color = (255, 255, 255) if Y < 0.5 else (0, 0, 0)

            # center of the tile
            cx = x + TILE_W // 2
            cy = y + TILE_H // 2

            out = draw_centered_text(out, name, (cx, cy), font, fill=text_color)

            # cv2.rectangle(out, (x, y), (x+TILE_W, y+TILE_H), (0,0,0), 1)

            x += TILE_W
        y += TILE_H

    cv2.imwrite(OUT_PATH, out)
    print(f"Saved: {OUT_PATH}")


if __name__ == "__main__":
    main()


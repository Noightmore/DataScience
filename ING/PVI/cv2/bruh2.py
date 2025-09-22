import os
from typing import Dict, Tuple, List
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

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

def main():

    for IN_PATH in ["../cv1/cv01_auto.jpg", "../cv1/cv01_jablko.jpg", "../cv1/cv01_mesic.jpg"]:
        colors = {}
        img = cv2.imread(IN_PATH, cv2.IMREAD_COLOR)

        if img is None:
            raise RuntimeError(f"Cannot read {IN_PATH}")
        H, W = img.shape[:2]
        total = H * W

        for y in range(H):
            for x in range(W):
                name = detect_color_name(img[y, x].tolist())
                if not name or name == "unknown":
                    continue
                colors[name] = colors.get(name, 0) + 1

        top3 = sorted(colors.items(), key=lambda kv: kv[1], reverse=True)[:3]

        # draw the results in top-left corner using PIL
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(rgb)
        draw = ImageDraw.Draw(im)
        font = try_load_comic_sans(max(18, W // 30))

        x0, y0 = 10, 10
        line_gap = font.size + 6

        # shadow + text for readability
        for i, (name, cnt) in enumerate(top3, start=1):
            line = f"{i}. {name}: {cnt} ({cnt * 100.0 / total:.1f}%)"
            # shadow
            draw.text((x0+1, y0+1), line, font=font, fill=(0, 0, 0))
            # main text
            draw.text((x0, y0), line, font=font, fill=(255, 255, 255))
            y0 += line_gap

        out_bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

        base = os.path.splitext(os.path.basename(IN_PATH))[0]
        out_path = os.path.join(os.path.dirname(IN_PATH), f"{base}_top3.png")
        cv2.imwrite(out_path, out_bgr)

        print(f"{IN_PATH} → top3:", top3, "| saved:", out_path)


if __name__ == "__main__":
    main()



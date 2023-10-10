import math

import cv2
import numpy as np
import matplotlib.pyplot as plt
import struct


def main():
    bgr = cv2.imread('cv03_objekty1.bmp')
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)

    plt.imshow(rgb)
    plt.colorbar()
    plt.show()

    height = bgr.shape[0]
    width = bgr.shape[1]

    # I = 0.3R + 0.59G + 0.11B  ????
    gray = cv2.cvtColor(bgr, cv2.COLOR_RGB2GRAY)

    plt.imshow(gray, cmap='gray')
    plt.colorbar()
    plt.show()

    image = load_bitmap_from_binary_file('cv03_objekty1.bmp')
    if image is not None:
        plt.imshow(image)
        plt.axis('off')
        plt.show()

    load_images_and_display_different_color_maps('cv03_objekty1.bmp')
    load_and_display_image_ycrcb('cv03_objekty1.bmp')
    plot_red_thing('cv03_red_object.jpg')


def load_bitmap_from_binary_file(path: str):
    with open(path, "rb") as f:
        bm = f.read(2)
        if bm != b'BM':
            raise Exception("not a BM")

        # Velikost souboru v bajtech
        size = struct.unpack('i', f.read(4))[0]
        # Rezerovavné bajty
        reserved = struct.unpack('i', f.read(4))[0]
        # Počet bajtů v hlavičce
        bytes_in_header = struct.unpack('i', f.read(4))[0]
        # Nějaký random bajty - nemaj žádnou funkci afaik
        _ = struct.unpack('i', f.read(4))[0]
        # Šířka obrázku v px
        width = struct.unpack('i', f.read(4))[0]
        # Výška obrázku v px
        height = struct.unpack('i', f.read(4))[0]
        # Počet ploch v obraze
        surfaces = struct.unpack("H", f.read(2))[0]
        # Počet bitů na pixel
        bits_per_pixel = struct.unpack("H", f.read(2))[0]
        # Typ komprese
        compression = struct.unpack('i', f.read(4))[0]
        # Velikost dat v bajtech
        data_size = struct.unpack('i', f.read(4))[0]
        # Horizontální počet pixelů na metr
        horizontal_pixels_per_meter = struct.unpack('i', f.read(4))[0]
        # Vertikální počet pixelů na metr
        vertical_pixels_per_meter = struct.unpack('i', f.read(4))[0]
        # Počet barev (pokud jsou definované)
        no_of_colors = struct.unpack('i', f.read(4))[0]
        # Počet důležitých barev (pokud jsou definované)
        no_of_important_colors = struct.unpack('i', f.read(4))[0]
        # Velikost jednoho řádku tak, aby byl dělitelný 4
        row_size = math.ceil(bits_per_pixel * width / 32) * 4
        # Převod z bitů na bajty (na pixel)
        bytes_per_pixel = int(bits_per_pixel / 8)
        # Inicializace obrazových dat
        image_data = np.ndarray((width, height, bytes_per_pixel), dtype="uint8")

        for row in image_data:
            col_index = 0
            for column in row:
                for channel in range(bytes_per_pixel):
                    column[channel] = struct.unpack('B', f.read(1))[0]
                    col_index += 1
            f.seek(abs(row_size - col_index), 1)

        # flip the image data horizontally
        image_data = np.flipud(image_data)

        return image_data


def load_images_and_display_different_color_maps(path: str):
    """
    COLOR_RGB2GRAY
    COLOR_RGB2HSV
    COLOR_COLOR_BGR2YCR_CB

    """
    try:
        # Load the image using cv2.imread()
        image = load_bitmap_from_binary_file(path)

        if image is None:
            raise Exception("Unable to read the image")

        # Convert the image to HSV color space
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Split the HSV image into H, S, and V channels
        h, s, v = cv2.split(hsv_image)

        # Display the original RGB image and its channels
        plt.figure(figsize=(12, 6))

        # Original RGB image
        plt.subplot(241)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title("RGB Image")
        plt.axis('off')

        # H (Hue) channel
        plt.subplot(242)
        plt.imshow(h, cmap='jet', vmin=0, vmax=179)
        plt.title("Hue (H)")
        plt.axis('off')
        plt.colorbar()

        # S (Saturation) channel
        plt.subplot(243)
        plt.imshow(s, cmap='jet', vmin=0, vmax=255)
        plt.title("Saturation (S)")
        plt.axis('off')
        plt.colorbar()

        # V (Value) channel
        plt.subplot(244)
        plt.imshow(v, cmap='jet', vmin=0, vmax=255)
        plt.title("Value (V)")
        plt.axis('off')
        plt.colorbar()

        plt.show()

    except Exception as e:
        print(f"Error: {e}")


def load_and_display_image_ycrcb(file_path):
    try:
        # Load the image using cv2.imread()
        image = load_bitmap_from_binary_file(file_path)

        if image is None:
            raise Exception("Unable to read the image")

        # Convert the image to YCrCb color space
        ycrcb_image = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)

        # Split the YCrCb image into Y, Cb, and Cr channels
        y, cb, cr = cv2.split(ycrcb_image)

        # Display the original RGB image and its channels
        plt.figure(figsize=(12, 6))

        # Original RGB image
        plt.subplot(241)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB))
        plt.title("RGB Image")
        plt.axis('off')

        # Y (Luma) channel
        plt.subplot(242)
        plt.imshow(y, cmap='gray', vmin=0, vmax=255)
        plt.title("Y (Luma)")
        plt.axis('off')
        plt.colorbar()

        # Cb (Chroma Blue) channel
        plt.subplot(243)
        plt.imshow(cb, cmap='jet', vmin=0, vmax=255)
        plt.title("Cb (Chroma Blue)")
        plt.axis('off')
        plt.colorbar()

        # Cr (Chroma Red) channel
        plt.subplot(244)
        plt.imshow(cr, cmap='jet', vmin=0, vmax=255)
        plt.title("Cr (Chroma Red)")
        plt.axis('off')
        plt.colorbar()

        plt.show()

    except Exception as e:
        print(f"Error: {e}")


def plot_red_thing(path: str):
    plt.figure("cv03_red_object.jpg")
    ball = cv2.cvtColor(cv2.imread("./cv03_red_object.jpg"), cv2.COLOR_BGR2RGB)
    ball2 = ball.copy()
    plt.subplot(1, 2, 1)
    plt.imshow(ball)

    rows, cols, _ = ball.shape

    # Thresholding podle zadání
    for i in range(rows):
        for j in range(cols):
            r, g, b = ball[i, j].tolist()

            try:
                thresh = r / (r + g + b)
                if thresh < 0.5:
                    ball2[i, j] = [255, 255, 255]
            except:
                continue

    plt.subplot(1, 2, 1)
    plt.imshow(ball)

    plt.subplot(1, 2, 2)
    plt.imshow(ball2)

    plt.show()


if __name__ == "__main__":
    main()

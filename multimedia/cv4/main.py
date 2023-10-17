from pathlib import Path

import cv2
import matplotlib.pyplot as plt


def main():
    """
        Hlavní funkce programu
    """
    images_etalons_mapping = {
        "./Cv04_porucha1.bmp": "./Cv04_porucha1_etalon.bmp",
        "./Cv04_porucha2.bmp": "./Cv04_porucha2_etalon.bmp"
    }

    # Jasová korekce obrázků
    for (source, error) in images_etalons_mapping.items():
        result = brightness_correction(Path(source), Path(error))

        plt.figure(f"Korekce obrázku {source}")

        plt.subplot(1, 3, 1)
        plt.imshow(result["original"])

        plt.subplot(1, 3, 2)
        plt.imshow(result["etalon"])

        plt.subplot(1, 3, 3)
        plt.imshow(result["corrected"])

        plt.show(block=False)

    # Ekvalizace histogramu
    her = histogram_equalization(Path("./Cv04_rentgen.bmp"))

    plt.figure("Ekvalizace histogramu obrázku")

    plt.subplot(2, 2, 1)
    plt.imshow(her["original"]["image"])

    plt.subplot(2, 2, 2)
    plt.xlim([0, 255])
    plt.xticks(ticks=range(0, 257, 16), labels=range(0, 257, 16))
    plt.yscale('log')
    plt.plot(her["original"]["histogram"])

    plt.subplot(2, 2, 3)
    plt.imshow(her["equalized"]["image"])

    plt.subplot(2, 2, 4)
    plt.xlim([0, 255])
    plt.xticks(ticks=range(0, 257, 16), labels=range(0, 257, 16))
    plt.yscale('log')
    plt.plot(her["equalized"]["histogram"])

    plt.show(block=False)


def brightness_correction(source: Path, error: Path, c=255):
    """Funkce pro jasovou korekci obrázku

    Args:
        source (Path): Cesta ke zkreslenému obrázku
        error (Path): Cesta k etalonu poruchy
        c (int, optional): Konstanta jasu. Defaults to 255.

    Raises:
        FileNotFoundError: _description_
    """

    if not source.exists() or not error.exists():
        raise FileNotFoundError()

    image = cv2.imread(source.as_posix())
    etalon = cv2.imread(error.as_posix())

    width = image.shape[0]
    height = image.shape[1]
    depth = image.shape[2]

    result = image.copy()

    for y in range(0, width):
        for x in range(0, height):
            for d in range(0, depth):
                result[y, x, d] = (c * image[y, x, d]) / (etalon[y, x, d])

    return {
        "original": image,
        "etalon": etalon,
        "corrected": result
    }


def histogram_equalization(source: Path):
    """Function for histogram equalization of images

    Args:
        source (Path): Path to the image

    Raises:
        FileNotFoundError: If the image path doesn't exist or is not a file

    Returns:
        dict: Dictionary with the original image, its histogram, and the equalized image and histogram
    """
    if not source.exists() or not source.is_file():
        raise FileNotFoundError()

    image = cv2.imread(source.as_posix())
    equalized = image.copy()

    # Calculate the histogram of the original image
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

    max_intensity = 255
    width, height, _ = image.shape

    # Initialize a cumulative histogram
    cumulative_histogram = [0] * 256
    cumulative_histogram[0] = histogram[0]

    # Calculate the cumulative histogram
    for i in range(1, 256):
        cumulative_histogram[i] = cumulative_histogram[i - 1] + histogram[i]

    # Normalize the cumulative histogram
    total_pixels = width * height
    normalized_histogram = [int((max_intensity / total_pixels) * val) for val in cumulative_histogram]

    # Apply histogram equalization to the equalized image
    for y in range(0, width):
        for x in range(0, height):
            intensity = image[y, x, 0]
            equalized[y, x] = normalized_histogram[intensity]

    # Calculate the histogram of the equalized image
    equalized_histogram = cv2.calcHist([equalized], [0], None, [256], [0, 256])

    return {
        "original": {
            "image": image,
            "histogram": histogram
        },
        "equalized": {
            "image": equalized,
            "histogram": equalized_histogram
        }
    }


if __name__ == "__main__":
    main()

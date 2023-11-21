import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load the image
#image = cv2.imread('Cv11_merkers.bmp', cv2.IMREAD_GRAYSCALE) # read image

# encode image using gradual erosion cv2.erode
# structural element is 3x3 matrix
# and decode the image using delatation cv2.dilate

# Display the image
#cv2.imshow('Image', image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


def calc_closest_factors(c: int):
    """Calculate the closest two factors of c.

    Returns:
      [int, int]: The two factors of c that are closest; in other words, the
        closest two integers for which a*b=c. If c is a perfect square, the
        result will be [sqrt(c), sqrt(c)]; if c is a prime number, the result
        will be [1, c]. The first number will always be the smallest, if they
        are not equal.
    """
    if c//1 != c:
        raise TypeError("c must be an integer.")

    a, b, i = 1, c, 0
    while a < b:
        i += 1
        if c % i == 0:
            a = i
            b = c//a

    return [b, a]


def encode_with_erosion(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE) / 255
    kernel = np.ones((3, 3), np.uint8)
    half_height = image.shape[0] // 2

    # Analyzované prvky v obrázku - horní a dolní polovina obrázku
    features = [image[:half_height, :], image[half_height:, :]]

    # Slovník grafů, které budou na konci procedury vykresleny.
    plots = {
        "Image": image,
    }

    # Analýza prvků
    for index, feature in enumerate(features):
        # Počet souřadnic prvků - počítáme s tím, že na konci bude jenom jedna
        coordinates_count = len(feature)
        # Počet iterací eroze
        iterations = 0
        # Kopie obrázku pro postupnou erozi
        encoded_image = feature.copy()

        # Nalezení počtu iterací nutných k zakódování
        while True:
            # Zakódování pomocí eroze
            temporary_image = cv2.erode(encoded_image, kernel)
            # Updatování počtu souřadnic
            coordinates_count = len(np.column_stack(np.where(temporary_image != 0)))

            # Pokud jsme ztratili informaci o značkách (a.k.a eroze odstranila už všechno)
            # Tak to přerušíme a necháme staré výsledky
            if coordinates_count == 0:
                break

            # Pokud ještě souřadnice zbyly, přičteme iteraci a nastavíme mezivýsledek
            iterations += 1
            encoded_image = temporary_image

        # Přidání zakódovaného obrázku do grafů
        plots[f"Feature {index} - Enkódovaný"] = encoded_image

        # Získání souřadnic značek
        coordinates = np.column_stack(np.where(encoded_image != 0))

        print("")
        print(f"Souřadnice značek (feature {index}): {coordinates[0]}")
        print(f"Počet iterací: {iterations}")
        print("")

        # Dekódování pomocí dilatace
        decoded_image = cv2.dilate(encoded_image, kernel, iterations=iterations)
        plots[f"Feature {index} - Dekódovaný"] = decoded_image

    # Vykreslení grafů
    plt.figure("Eroze a dilatace")
    subplot_factors = calc_closest_factors(len(plots.keys()))
    index = 1

    for label, image_data in plots.items():
        plt.subplot(subplot_factors[0], subplot_factors[1], index)
        plt.title(label)
        plt.imshow(image_data, cmap="gray")

        index += 1

    # Ukázání okna s grafy
    plt.show()


encode_with_erosion("Cv11_merkers.bmp")

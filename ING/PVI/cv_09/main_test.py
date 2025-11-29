import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr
from pytesseract import pytesseract

# Načtení vzorového obrazu občanského průkazu
image_template = cv2.imread('pvi_cv09/obcansky_prukaz_cr_sablona_2012_2014.png', cv2.IMREAD_GRAYSCALE)
image_template = cv2.resize(image_template, (image_template.shape[0]*2, image_template.shape[1]*2))
plt.imshow(image_template)
plt.show()
# Načtení testovacího obrazu
test_image = cv2.imread('pvi_cv09/test/TS10_01.jpg')
# Zkontroluj, že obrázky byly načteny správně
if image_template is None or test_image is None:
    print("Chyba při načítání obrázků!")
else:
    print("Obrázky byly úspěšně načteny.")

# SIFT pro detekci a extrakci deskriptorů
sift = cv2.SIFT_create()
keypoints_template, descriptors_template = sift.detectAndCompute(image_template, None)
keypoints_test, descriptors_test = sift.detectAndCompute(cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY), None)

# Porovnání deskriptorů
bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
matches = bf.knnMatch(descriptors_template, descriptors_test, k=2)

# Filtrování dobrých shod
good_matches = [m for m, n in matches if m.distance < 0.8 * n.distance]

# Pokud nejsou dobré shody, vypiš varování
print(f'Počet dobrých shod: {len(good_matches)}')
if len(good_matches) == 0:
    print("Nebyla nalezena žádná dobrá shoda mezi obrázky!")

# Odhadnutí projektivní transformace
if len(good_matches) > 0:
    points_template = np.float32([keypoints_template[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    points_test = np.float32([keypoints_test[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Odhadnutí projektivní transformace
    matrix, mask = cv2.findHomography(points_template, points_test, cv2.RANSAC)

    # Aplikování transformace na rohy vzorového obrazu
    height, width = image_template.shape
    corners = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]]).reshape(-1, 1, 2)
    transformed_corners = cv2.perspectiveTransform(corners, matrix)

    # Transformace rohů vzorového obrazu
    h, w = image_template.shape
    aligned_img = cv2.warpPerspective(test_image, np.linalg.inv(matrix), (w, h))

    # Zobrazení výsledného obrazu
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(aligned_img, cv2.COLOR_BGR2RGB))
    plt.title("Zarovnaný Občanský Průkaz")
    plt.show()

    # Definování oblastí pro jméno, příjmení a fotku
    roi_name = np.array([77, 51, 130, 69])   # (x_min, y_min, x_max, y_max)
    roi_surname = np.array([72, 37, 130, 55])
    roi_photo = np.array([10, 70, 120, 210])
    aligned_img = cv2.cvtColor(aligned_img, cv2.COLOR_BGR2GRAY)
    # Oříznutí jednotlivých oblastí ROI
    name_roi = aligned_img[roi_name[1]:roi_name[3], roi_name[0]:roi_name[2]]
    surname_roi = aligned_img[roi_surname[1]:roi_surname[3], roi_surname[0]:roi_surname[2]]
    photo_roi = aligned_img[roi_photo[1]:roi_photo[3], roi_photo[0]:roi_photo[2]]


    # Inicializace EasyOCR
    reader = easyocr.Reader(['en'], gpu=True)
    name_text = reader.readtext(surname_roi.astype("uint8"), detail=0)
    surname_text = reader.readtext(name_roi.astype("uint8"), detail=0)
    # # Zobrazení extrahovaných textů
    print("Jméno:", " ".join(name_text))
    print("Příjmení:", " ".join(surname_text))

    # Zobrazení samotného oříznutého obrazu pro jméno, příjmení a fotku
    plt.figure(figsize=(12, 8))

    # Zobrazení oblasti pro jméno
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(name_roi, cv2.COLOR_BGR2RGB))
    plt.title("Oříznuté jméno")
    plt.axis('off')

    # Zobrazení oblasti pro příjmení
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(surname_roi, cv2.COLOR_BGR2RGB))
    plt.title("Oříznuté příjmení")
    plt.axis('off')

    # Zobrazení oblasti pro fotku
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(photo_roi, cv2.COLOR_BGR2RGB))
    plt.title("Oříznutá fotka")
    plt.axis('off')

    plt.show()

else:
    print("Nejsou nalezeny žádné odpovídající shody pro homografii.")
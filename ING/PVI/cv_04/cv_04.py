import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def amplitude_spectrum(gray_float64):
    eps = 1e-8
    F = np.fft.fft2(gray_float64)
    Fshift = np.fft.fftshift(F)
    mag = np.abs(Fshift)
    log_mag = np.log(mag + eps)
    log_mag -= log_mag.min()
    if log_mag.max() > 0:
        log_mag /= log_mag.max()
    return log_mag

def own_median_5x5(gray_uint8):
    k = 5
    r = k // 2  # 2
    # padding
    padded = cv2.copyMakeBorder(gray_uint8, r, r, r, r, borderType=cv2.BORDER_REFLECT)
    h, w = gray_uint8.shape
    out = np.empty_like(gray_uint8)
    # pro každý pixel vyber okno 5x5 a spočítej median
    for y in range(h):
        for x in range(w):
            win = padded[y:y+k, x:x+k]
            out[y, x] = np.median(win)
    return out

def plot_image_hist_spectrum(ax_img, ax_hist, ax_spec, img_uint8, title_img):
    # obraz
    ax_img.imshow(img_uint8, cmap='gray', vmin=0, vmax=255)
    ax_img.set_title(title_img, fontsize=10)
    ax_img.axis('off')
    # histogram
    ax_hist.hist(img_uint8.ravel(), bins=256, range=(0,255))
    ax_hist.set_title('Histogram', fontsize=9)
    ax_hist.set_xlim(0,255)
    # spektrum
    spec = amplitude_spectrum(img_uint8.astype(np.float64)/255.0)
    ax_spec.imshow(spec, cmap='gray', vmin=0, vmax=1)
    ax_spec.set_title('Amplitudové spektrum', fontsize=9)
    ax_spec.axis('off')

def binarize_otsu(gray_uint8):
    # Otsu pro původní obraz (automatický práh)
    _, bin_im = cv2.threshold(gray_uint8, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return bin_im

def one_count(bin_uint8):
    # Převede 255->1, 0->0 a sečte
    return int((bin_uint8 > 0).sum())


IMG_DIR = Path("/Users/mothspaws/Desktop/NS3.semestr/PVI/cv_04/PVI_C04")
task1_name = "pvi_cv04.png"
task2_names = [
    "pvi_cv04_im01.png",
    "pvi_cv04_im02.png",
    "pvi_cv04_im03.png",
    "pvi_cv04_im04.png",
    "pvi_cv04_im05.png",
    "pvi_cv04_im06.png",
]

# 1
im_bgr = cv2.imread(str(IMG_DIR / task1_name), cv2.IMREAD_COLOR)
if im_bgr is None:
    raise FileNotFoundError(f"Soubor {IMG_DIR / task1_name} nebyl nalezen.")
gray = cv2.cvtColor(im_bgr, cv2.COLOR_BGR2GRAY)

averIm = cv2.blur(gray, (3,3))
medIm_cv = cv2.medianBlur(gray, 5)
medIm_own = own_median_5x5(gray)

# 1A) Zobrazení: původní, průměrovací filtr, median (OpenCV) – každý s histogramem a spektrem
fig1, axes1 = plt.subplots(3, 3, figsize=(12, 10))
plot_image_hist_spectrum(axes1[0,0], axes1[0,1], axes1[0,2], gray,       "Původní (šedotón)")
plot_image_hist_spectrum(axes1[1,0], axes1[1,1], axes1[1,2], averIm,     "Průměrovací filtr 3×3 (cv2.blur)")
plot_image_hist_spectrum(axes1[2,0], axes1[2,1], axes1[2,2], medIm_cv,   "Medián 5×5 (cv2.medianBlur)")
fig1.suptitle("Úkol 1: Odstranění šumu + histogramy + amplitudová spektra", fontsize=12)
fig1.tight_layout()

# 1B) Porovnání: vlastní median 5×5 vs. OpenCV median
fig2, axes2 = plt.subplots(1, 3, figsize=(12, 4))
axes2[0].imshow(medIm_cv, cmap='gray', vmin=0, vmax=255); axes2[0].set_title("cv2.medianBlur 5×5"); axes2[0].axis('off')
axes2[1].imshow(medIm_own, cmap='gray', vmin=0, vmax=255); axes2[1].set_title("Vlastní median 5×5"); axes2[1].axis('off')
diff = cv2.absdiff(medIm_cv, medIm_own)
axes2[2].imshow(diff, cmap='gray', vmin=0, vmax=255); axes2[2].set_title(f"Rozdíl |cv - own|\nmax={diff.max()} mean={diff.mean():.2f}")
axes2[2].axis('off')
fig2.suptitle("Úkol 1: Srovnání medianů (OpenCV vs. vlastní 5×5)", fontsize=12)
fig2.tight_layout()

# 2
# Načti 6 obrázků, převed' na šedotón, detekuj Canny,
# původní i Canny převést na binární, spočítat sumu jedniček a dát do title.
ims_gray = []
ims_bin = []
ims_edges = []
ims_edges_bin = []
filenames = []

for name in task2_names:
    p = IMG_DIR / name
    bgr = cv2.imread(str(p), cv2.IMREAD_COLOR)
    if bgr is None:
        raise FileNotFoundError(f"Soubor {p} nebyl nalezen.")
    g = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    # binarizace původního (Otsu)
    g_bin = binarize_otsu(g)
    # Canny (nastavení lze upravit dle požadavků)
    edges = cv2.Canny(g, 100, 256)  # jak v zadání
    # Canny výstup je 0/255 -> už je „binární“ v 8bit; ponecháme tak
    ims_gray.append(g)
    ims_bin.append(g_bin)
    ims_edges.append(edges)
    ims_edges_bin.append(edges)
    filenames.append(name)
fig3, axes3 = plt.subplots(2, 6, figsize=(18, 6))
for i in range(6):
    # horní řada: původní binární
    ones_orig = one_count(ims_bin[i])
    axes3[0, i].imshow(ims_bin[i], cmap='gray', vmin=0, vmax=255)
    axes3[0, i].set_title(f"{filenames[i]}\nOrig bin: ones={ones_orig}", fontsize=9)
    axes3[0, i].axis('off')

    # dolní řada: Canny binární
    ones_edges = one_count(ims_edges_bin[i])
    axes3[1, i].imshow(ims_edges_bin[i], cmap='gray', vmin=0, vmax=255)
    axes3[1, i].set_title(f"Canny bin: ones={ones_edges}", fontsize=9)
    axes3[1, i].axis('off')

fig3.suptitle("Úkol 2: Binarizace originálu (Otsu) a Canny (+ počty jedniček) – vše v jednom okně", fontsize=12)
fig3.tight_layout()

plt.show()

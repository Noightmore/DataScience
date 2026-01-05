import cv2
import numpy as np
from matplotlib import pyplot as plt

def four_plot(imgs,labels):
    plt.figure(figsize=(8, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(imgs[0])
    plt.title(labels[0])
    plt.axis('off')

    plt.subplot(2, 2, 2)
    # plt.imshow(imgs[1], cmap='hsv')
    plt.imshow(imgs[1], cmap='jet')
    plt.colorbar()
    plt.title(labels[1])
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.plot(imgs[2], color='blue')
    plt.title(labels[2])
    plt.xlim([0, 256])

    plt.subplot(2, 2, 4)
    # plt.imshow(imgs[3], cmap='gray')
    plt.imshow(imgs[3], cmap='jet')
    plt.colorbar()
    plt.title(labels[3])
    plt.axis('off')

    plt.tight_layout()
    plt.show()

def apply_watershed_and_dilate(thresh_img, original_img):
    kernel = np.ones((3, 3), np.uint8)

    opening = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3) # roztahnu pozadi

    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5) # kazdemu bilemu reknu jak dalekko je od nejblizsi cerne
    _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    _, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1 # pro pozadi
    markers[unknown == 255] = 0

    # Apply watershed algorithm
    markers = cv2.watershed(original_img, markers)
    original_img[markers == -1] = [255, 0, 0]  # cervena hranice

    dilated_boundaries = cv2.dilate((markers == -1).astype(np.uint8), kernel, iterations=1) # rozsirim hraze
    separated_objects = cv2.bitwise_and(opening, opening, mask=(1 - dilated_boundaries))
    return dist_transform, sure_fg, unknown, markers, dilated_boundaries,separated_objects

def six_plot(imgs, labels):
    plt.figure(figsize=(12, 8))

    for i in range(6):
        plt.subplot(2, 3, i + 1)
        plt.imshow(imgs[i], cmap='jet' if i in [0, 2, 3, 4, 5] else 'gray')
        plt.title(labels[i])
        plt.colorbar()
        plt.axis('off')

    plt.tight_layout()
    plt.show()

def remove_small_objects(binary_image, min_size=1000):
    num_labels, labels_im = cv2.connectedComponents(binary_image)
    output_image = np.zeros_like(binary_image)

    for label in range(1, num_labels):
        component_size = np.sum(labels_im == label)
        if component_size >= min_size:
            output_image[labels_im == label] = 255

    return output_image

def granulometry(bin_im,start_size = 40):
    gran_img = np.zeros(bin_im.shape)
    prev_op = bin_im.copy()
    cnt = 0
    for i in range(1, 100):
        kernel = np.ones((i, i), np.uint8)
        opening = cv2.morphologyEx(bin_im,cv2.MORPH_OPEN,kernel)
        gran_img[opening != prev_op] = i
        prev_op = opening.copy()
        cnt += 1
        if np.sum(opening) == 0:
            break

    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    im = ax[0].imshow(gran_img, cmap='jet')
    fig.colorbar(im, ax=ax[0])
    ax[0].set_title('Gran')

    gran_img = gran_img.astype(int)
    hist = np.bincount(gran_img.astype(int).flatten())
    for i in range(start_size, cnt):
        ratio = hist[i] / i**2
        if ratio > 0.9:
            ratio = np.floor(ratio).astype(int)
            print('No. objects: ',ratio,'size:', i, 'x', i)

    im = ax[1].plot(range(start_size, cnt), hist[range(start_size, cnt)])
    ax[1].set_title('Hist')

    plt.show()
    return



if __name__ == '__main__':
    bgr = cv2.imread("pvi_cv06_mince.jpg")
    rgb_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    hsv_image = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hue_image = hsv_image[:, :, 0]
    hist, bins = np.histogram(hue_image.ravel(), 256, [0, 256])
    _, thresholded_image = cv2.threshold(hue_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresholded_image = 255 - thresholded_image
    kernel = np.ones((5, 5), np.uint8)


    four_plot([rgb_image, hue_image, hist, thresholded_image],['RGB Image','Hue Image','Histogram of Hue','Segmented Image'])
    dist_transform, sure_fg, unknown, markers, dilated_boundaries, separated_objects = apply_watershed_and_dilate(thresholded_image,bgr)
    separated_objects = remove_small_objects(separated_objects)
    six_plot([dist_transform, sure_fg, unknown, markers, dilated_boundaries, separated_objects],
             ['Distance Transform', 'Foreground', 'Unknown', 'Markers', 'Watershed Border',
              'Binary Image with Watershed'])


    ### GRANU ###
    bin_granu = separated_objects
    #true_binary_image = (bin_granu // 255).astype(np.uint8)
    granulometry(bin_granu)


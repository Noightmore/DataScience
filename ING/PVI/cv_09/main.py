import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.feature import match_descriptors, SIFT
#from skimage.feature import plot_matches as plot_matches
from skimage.measure import ransac
from skimage.transform import ProjectiveTransform, warp
import os
from skimage import feature
import easyocr


def load_sift(path):
    img_vzor = cv2.imread(path)
    # Convert to grayscale
    vzor_gray = cv2.cvtColor(img_vzor, cv2.COLOR_BGR2GRAY)
    # Initialize SIFT detector and extract keypoints and descriptors
    descriptor_extractor = SIFT()
    descriptor_extractor.detect_and_extract(vzor_gray)
    keypoints = descriptor_extractor.keypoints
    descriptors = descriptor_extractor.descriptors
    return keypoints, descriptors, img_vzor


def find_and_filter_matches(descriptors1, descriptors2):
    # Find matches and filter using cross-check
    matches = match_descriptors(descriptors1, descriptors2, cross_check=True, metric='euclidean')
    return matches


def estimate_transform(keypoints1, keypoints2, matches):
    # Extract matched keypoints
    src = keypoints1[matches[:, 0]]
    dst = keypoints2[matches[:, 1]]
    # Use RANSAC to find a robust projective transform
    model, inliers = ransac((src, dst), ProjectiveTransform, min_samples=4, residual_threshold=2, max_trials=500)
    return model, inliers


def extract_id_card(img_test, model, img_vzor):
    # Get image dimensions of vzor (template)
    h, w = img_vzor.shape[:2]
    # Define corners in the template image
    corners = np.array([[0, 0], [w, 0], [w, h], [0, h]])
    # Transform corners to test image using the model
    warped_corners = model(corners)
    # Warp the test image to align with template
    warped_img = warp(img_test, model.inverse, output_shape=(h, w))
    return warped_img, warped_corners




if __name__ == '__main__':
    keypoints_vzor, descriptors_vzor, img_vzor = load_sift("pvi_cv09/obcansky_prukaz_cr_sablona_2012_2014.png")
    directory = "pvi_cv09/test/"

    test_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if
                  filename.endswith(('.jpg', '.png'))]

    for path in test_paths:
        keypoints_test, descriptors_test, img_test = load_sift(path)
        matches = find_and_filter_matches(descriptors_vzor, descriptors_test)

        model, inliers = estimate_transform(keypoints_vzor, keypoints_test, matches)

        # Display inlier matches for visualization
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        feature.plot_matches(ax[0], rgb2gray(img_vzor), rgb2gray(img_test), keypoints_vzor, keypoints_test, matches[inliers])
        ax[0].set_title("Filtered Matches Between Vzor and Test Image")
        ax[0].axis("off")

        # Extract and align the ID card from test image -- chyba je v této části
        warped_img, warped_corners = extract_id_card(img_test, model, img_vzor)

        # Display aligned ID card
        ax[1].imshow(warped_img)
        ax[1].set_title("Aligned ID Card")
        ax[1].axis("off")
        plt.show()


import numpy as np
import cv2
import matplotlib.pyplot as plt


def calculate_closest_factors(c: int):
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
            b = c // a

    return [b, a]


def encode_with_erosion(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE) / 255
    kernel = np.ones((3, 3), np.uint8)
    half_height = image.shape[0] // 2

    # Analyzed elements in the image - top and bottom half of the image
    features = [image[:half_height, :], image[half_height:, :]]

    # Dictionary of graphs that will be drawn at the end of the procedure.
    plots = {
        "Image": image,
    }

    # Analysis of elements
    for index, feature in enumerate(features):
        # Number of element coordinates - we assume that there will be only one at the end
        coordinates_count = len(feature)
        # Number of erosion iterations
        iterations = 0
        # Copy of the image for gradual erosion
        encoded_image = feature.copy()

        # Find the number of iterations needed for encoding
        while True:
            # Encoding using erosion
            temporary_image = cv2.erode(encoded_image, kernel)
            # Updating the number of coordinates
            coordinates_count = len(np.column_stack(np.where(temporary_image != 0)))

            # If we have lost the information about the marks (i.e., erosion has removed everything)
            # Then we break it and leave the old results
            if coordinates_count == 0:
                break

            # If there are still coordinates left, we add an iteration and set the interim result
            iterations += 1
            encoded_image = temporary_image

        # Adding the encoded image to the graphs
        plots[f"Part {index} - Encoded"] = encoded_image

        # Getting the coordinates of the marks
        coordinates = np.column_stack(np.where(encoded_image != 0))

        print("-------------------------------------------------------")
        print(f"Coordinates index (part {index}): {coordinates[0]}")
        print(f"Iteration count: {iterations}")
        print("-------------------------------------------------------")

        # Decoding using dilation
        decoded_image = cv2.dilate(encoded_image, kernel, iterations=iterations)
        plots[f"Part {index} - Decoded"] = decoded_image

    plt.figure("Erosion and Dilation")

    # Create figures for each image
    for label, image_data in plots.items():
        plt.figure()  # Create a new figure for each image
        plt.title(label)
        plt.imshow(image_data, cmap="gray")
        plt.axis("off")

        # Rotate x-axis labels
        plt.xticks(rotation=45)

        # Show the window with the current image
        plt.show()

    # Combine the two images feature 0 and feature 1
    # and display the result
    plt.figure("Combined")
    plt.title("Combined")
    plt.imshow(np.vstack((plots["Part 0 - Decoded"], plots["Part 1 - Decoded"])), cmap="gray")
    plt.axis("off")
    plt.xticks(rotation=45)
    plt.show()


if __name__ == "__main__":
    encode_with_erosion("Cv11_merkers.bmp")

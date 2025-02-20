import cv2
import numpy as np

# using hough circles to detect count of circles in the image

img1 = cv2.imread('Cv11_c01.bmp', cv2.IMREAD_GRAYSCALE)  # read image
img2 = cv2.imread('Cv11_c02.bmp', cv2.IMREAD_GRAYSCALE)  # read image
img3 = cv2.imread('Cv11_c03.bmp', cv2.IMREAD_GRAYSCALE)  # read image
img4 = cv2.imread('Cv11_c04.bmp', cv2.IMREAD_GRAYSCALE)  # read image
img5 = cv2.imread('Cv11_c05.bmp', cv2.IMREAD_GRAYSCALE)  # read image
img6 = cv2.imread('Cv11_c06.bmp', cv2.IMREAD_GRAYSCALE)  # read image

images = [img1, img2, img3, img4, img5, img6]


def detect_circles(image):
    # Apply GaussianBlur to reduce noise and help the circle detection
    blurred_image = cv2.GaussianBlur(image, (9, 9), 2)

    # Use HoughCircles to detect circles in the image
    circles = cv2.HoughCircles(
        blurred_image,
        cv2.HOUGH_GRADIENT,
        dp=1,  # Resolution of accumulator ratio (1 for input image resolution)
        minDist=50,  # Minimum distance between detected circles
        param1=50,   # Upper threshold for the internal Canny edge detector
        param2=30,   # Threshold for center detection (lower means more false circles)
        minRadius=10,  # Minimum radius of the circles
        maxRadius=100  # Maximum radius of the circles
    )

    if circles is not None:
        # Convert circle coordinates to integers
        circles = np.uint16(np.around(circles))

        # Draw the circles on the original image
        for i in circles[0, :]:
            cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)  # Draw the outer circle
            cv2.circle(image, (i[0], i[1]), 2, (0, 0, 255), 3)  # Draw the center of the circle

        # Get the number of circles detected
        num_circles = len(circles[0])

        # Write the circle count to the middle of the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text = f"{num_circles}"
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_position = ((image.shape[1] - text_size[0]) // 2, image.shape[0] // 2)
        cv2.putText(image, text, text_position, font, font_scale, (102, 255, 107), font_thickness)

        # Display the image with detected circles and circle count
        cv2.imshow('Detected Circles', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Return the number of circles detected
        return num_circles
    else:
        print("No circles detected in the image.")
        return 0


# Loop through each image and apply circle detection
for image in images:
    # Convert the image to grayscale if it's not already
    if len(image.shape) > 2:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray_image = image

    # Detect circles in the current image
    num_circles = detect_circles(gray_image)

    # Print the number of circles detected in the current image
    print(f"Number of circles detected: {num_circles}")



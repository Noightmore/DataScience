import cv2
import numpy as np
import matplotlib.pyplot as plt


image = cv2.imread('Cv04_porucha1.bmp')

# Ensure the image loaded successfully
if image is not None:
    # Display the image using Matplotlib
    plt.figure(figsize=(8, 6))  # Set the figure size
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # Convert BGR to RGB for Matplotlib
    plt.axis('off')  # Turn off axis labels

    # Add a title (optional)
    plt.title('Image Title')

    # Show the image figure
    plt.show()
else:
    print("Unable to load the image.")

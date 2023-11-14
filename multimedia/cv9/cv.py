import cv2
import numpy as np
import matplotlib.pyplot as plt


def pca_manual(image_path, num_components=3):
    # Step 1: Read Image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Step 2: Convert image to a 2D array
    data = image.reshape(-1, 3)

    # Step 3: Mean Centering
    mean_vector = np.mean(data, axis=0)
    mean_centered_data = data - mean_vector

    # Step 4: Compute Covariance Matrix
    covariance_matrix = np.cov(mean_centered_data, rowvar=False)

    # Step 5: Compute Eigenvectors and Eigenvalues
    eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)

    # Step 6: Sort Eigenvectors
    sorted_indices = np.argsort(eigenvalues)[::-1]
    sorted_eigenvectors = eigenvectors[:, sorted_indices]

    # Step 7: Select Principal Components
    principal_components = sorted_eigenvectors[:, :num_components]

    # Step 8: Transform the Data
    transformed_data = np.dot(mean_centered_data, principal_components)

    # Optional: Inverse transform to reconstruct the data
    reconstructed_data = np.dot(transformed_data, principal_components.T)

    # Reshape the data back to the original image shape
    reconstructed_image = reconstructed_data.reshape(image.shape).astype(np.uint8)

    # Save or display the reconstructed image
    return reconstructed_image


def main():
    image = cv2.imread("./Cv09_obr.bmp")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    width = image.shape[0]
    height = image.shape[1]

    result = pca_manual("./Cv09_obr.bmp", 3)

    #print(result, result.shape)
    plt.figure("Komponenty PCA")
    plt.subplot(2, 2, 1)
    plt.title("Původní obrázek")
    plt.imshow(image)

    plt.show(block=False)

    plt.figure("Porovnání")
    plt.subplot(2, 2, 1)
    plt.title("Výsledek PCA")
    plt.imshow(result, cmap="gray")

    plt.subplot(2, 2, 2)
    plt.title("Výsledek RGB2GRAY")
    plt.imshow(cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY), cmap="gray")

    plt.subplot(2,2,3)
    plt.title("Histogram PCA")
    plt.hist(result[0], bins=256)

    plt.subplot(2,2,4)
    plt.title("Histogram RGB2GRAY")
    plt.hist(cv2.cvtColor(image.copy(), cv2.COLOR_RGB2GRAY).ravel(), bins=256)

    plt.show()


if __name__ == "__main__":
    main()




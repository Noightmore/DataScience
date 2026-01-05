import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

if __name__ == '__main__':
    unknown = cv2.imread("unknown.bmp")
    unknown = cv2.cvtColor(unknown, cv2.COLOR_BGR2GRAY)
    directory_path = "data/"
    image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")
    image_paths = [
        os.path.join(directory_path, file)
        for file in os.listdir(directory_path)
        if file.lower().endswith(image_extensions)
    ]
    CNT = 0
    X = np.zeros((4096, 3), dtype=complex)

    for path in image_paths:

        img_class = cv2.imread(path)
        imG = cv2.cvtColor(img_class, cv2.COLOR_BGR2GRAY)
        vec = np.fft.fft2(imG).flatten()
        if CNT == 2: ## main code for 3 img MACE
            X[:,CNT] = vec
            power_spec = np.mean((np.abs(X) ** 2), axis=1)
            D = np.diag(power_spec)
            Dm1 = np.linalg.inv(D)

            Xp = X.conjugate().transpose()
            u = np.ones([3,1])
            H = Dm1 @ X @ np.linalg.inv(Xp @ Dm1 @ X) @ u
            h_mace = H.reshape(64, 64)
            ##classify


            unknown_fft = np.fft.fft2(unknown)
            M = np.conj(h_mace) * unknown_fft
            response = np.fft.ifft2(M) # Correlation output
            response = np.abs(np.fft.fftshift(response))

            ## RESI calc ##

            peak_y, peak_x = np.unravel_index(np.argmax(response), response.shape)

            # Define the size of O (20x20) and V (10x10)
            O_size = 20
            V_size = 10
            half_O = O_size // 2
            half_V = V_size // 2

            # Extract the O region centered on the peak
            y_start = max(0, peak_y - half_O)
            y_end = min(response.shape[0], peak_y + half_O)
            x_start = max(0, peak_x - half_O)
            x_end = min(response.shape[1], peak_x + half_O)
            O_region = response[y_start:y_end, x_start:x_end]

            # Extract the V region within O
            Vy_start = max(0, peak_y - half_V)
            Vy_end = min(response.shape[0], peak_y + half_V)
            Vx_start = max(0, peak_x - half_V)
            Vx_end = min(response.shape[1], peak_x + half_V)
            V_region = response[Vy_start:Vy_end, Vx_start:Vx_end]

            # Calculate mean and standard deviation of O excluding V
            O_flat = O_region.flatten()
            V_flat = V_region.flatten()
            O_minus_V = np.setdiff1d(O_flat, V_flat)


            O_mean = np.mean(O_minus_V)
            O_std = np.std(O_minus_V)
            # Calculate RES_i
            V_max = np.max(V_region)
            RES_i = (V_max - O_mean) / O_std
            print(RES_i)

            # Visualization of results
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            # Plot the correlation output heatmap
            axes[0, 0].imshow(response, cmap="jet")
            axes[0, 0].set_title("Correlation Output Heatmap")
            axes[0, 1].imshow(np.abs(np.fft.ifft2(h_mace)), cmap="jet")
            axes[0, 1].set_title("MACE Filter (Magnitude)")
            # 3D plots of the same
            ax1 = fig.add_subplot(2, 2, 3, projection="3d")
            X_grid, Y_grid = np.meshgrid(np.arange(64), np.arange(64))
            ax1.plot_surface(X_grid, Y_grid, response, cmap="jet")
            ax1.set_title("3D Correlation Output")
            ax2 = fig.add_subplot(2, 2, 4, projection="3d")
            ax2.plot_surface(X_grid, Y_grid, np.abs(np.fft.ifft2(h_mace)), cmap="jet")
            ax2.set_title("3D MACE Filter")
            plt.tight_layout()
            plt.show()


            CNT = 0
        else:
            X[:,CNT] = vec
            CNT += 1

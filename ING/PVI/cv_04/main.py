import cv2
import numpy as np
from matplotlib import pyplot as plt

files = ["PVI_C04/pvi_cv04_im01.png",
         "PVI_C04/pvi_cv04_im02.png",
         "PVI_C04/pvi_cv04_im03.png",
         "PVI_C04/pvi_cv04_im04.png",
         "PVI_C04/pvi_cv04_im05.png",
         "PVI_C04/pvi_cv04_im06.png"]

def circle_or_square(edge_img):
        top_edge_row = None
        image_width = edges.shape[1]
        for row_idx in range(edge_img.shape[0]):
                if np.count_nonzero(edge_img[row_idx]) > 0:
                        top_edge_row = row_idx
                        break
        consecutive_edges = 0
        if top_edge_row is not None:
                row_data = edges[top_edge_row]
                consecutive_edges = np.count_nonzero(row_data)
        percentage_edge_in_row = (consecutive_edges / image_width) * 100

        if percentage_edge_in_row > 30:
                print(f"Detected Shape: Square (Edge pixels: {percentage_edge_in_row:.2f}%)")
                return "square"
        else:
                print(f"Detected Shape: Circle (Edge pixels: {percentage_edge_in_row:.2f}%)")
                return "circle"

if __name__ == '__main__':
        fig, axes = plt.subplots(2, 6, figsize=(18, 8))
        for i, (ax, file) in enumerate(zip(axes.flatten(), files * 2)):
            bgr = cv2.imread(file)
            if bgr is not None:
                if i < 6:
                    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
                    ax.imshow(gray,cmap="jet")
                    white_pixel_count = cv2.countNonZero(gray)
                    ax.set_title(f"White pixels: {white_pixel_count}", fontsize=10)

                else:
                    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray, 100, 200)
                    print(edges.shape)
                    tit = circle_or_square(edges)
                    white_pixel_count = cv2.countNonZero(edges)

                    ax.imshow(edges, cmap="jet")

                    ax.set_title(f"W: {white_pixel_count}, {tit}", fontsize=10)

                ax.axis('off')


        plt.tight_layout()
        plt.show()

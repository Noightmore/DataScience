import numpy as np
import cv2
from typing import List, Tuple, Dict, NoReturn, Any
from collections import deque
import matplotlib.pyplot as plt
from cassandra.util import long


class ImageProcessor:
    def __init__(self, image_path: str):
        """
        Initialize the ImageProcessor instance by loading an image from the specified path and
        converting it to the RGB color space.

        Args:
            image_path (str): Path to the image file to be loaded and processed.
        """
        self.image = cv2.imread(image_path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    @staticmethod
    def compute_smooth_histogram(image: np.ndarray, smooth_factor: int = 1) -> np.ndarray:
        """
        Calculate a smoothed histogram for the provided image. The histogram is first computed,
        normalized, and then smoothed using a convolution with a uniform kernel defined by the smooth_factor.

        Args:
            image (np.ndarray): The image array for which the histogram is to be computed.
            smooth_factor (int): The size of the smoothing window, which affects the degree of smoothing.

        Returns:
            np.ndarray: A 1D array representing the smoothed histogram of the image.
        """

        histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
        normalized_histogram = (histogram / histogram.max()) * 255
        flat_histogram = normalized_histogram.flatten()
        smoothing_window = np.ones(smooth_factor) / smooth_factor
        return np.convolve(flat_histogram, smoothing_window, mode='same')

    @staticmethod
    def find_first_local_minimum(data: np.ndarray) -> np.ndarray[Any, np.dtype[np.signedinteger[Any] | long]]:
        """
        Identify and return the index of the first local minimum in a 1D array. A local minimum is defined
        as a point which is lower than its immediate neighbors.

        Args:
            data (np.ndarray): The 1D array from which to find the first local minimum.

        Returns:
            int: The index of the first local minimum in the array.

        Raises:
            ValueError: If no local minimum is found, indicating a potential issue with the data or its processing.
        """
        local_minima_indices = np.where((data[1:-1] < data[:-2]) & (data[1:-1] < data[2:]))[0]
        if local_minima_indices.size == 0:
            raise ValueError("No local minimum found in the array.")
        return local_minima_indices[0]

    @staticmethod
    def calculate_region_centroids(segmented_image: np.ndarray) -> List[List[int]]:
        """
        Calculate and return a list of centroids for all labeled regions in a segmented image.
        Each region is assumed to be labeled with a unique integer, and the background is labeled as 0.

        Args:
            segmented_image (np.ndarray): An image array where each region is labeled with integers.

        Returns:
            List[List[int]]: A list of centroids, where each centroid is a list [x, y] coordinates.

        Raises:
            ValueError: If the segmented image has no objects or a region
            has zero area which would cause division by zero.
        """

        if np.max(segmented_image) == 0:
            raise ValueError("The segmented image contains no objects to process.")

        centroids = []
        for label in range(2, np.max(segmented_image) + 1):
            mask = np.zeros_like(segmented_image)
            mask[segmented_image == label] = 1
            moments = cv2.moments(mask, binaryImage=True)
            if moments['m00'] == 0:
                raise ValueError(f"Region with label {label} has zero area, can't compute centroid.")
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            centroids.append([cx, cy])
        return centroids

    @staticmethod
    def label_image_regions(image: np.ndarray) -> np.ndarray:
        """
       Label connected regions in a binary image. This function performs a breadth-first search to
       label all connected components of the foreground (non-zero pixels).

       Args:
           image (np.ndarray): A binary image where the foreground is represented by 1's and background by 0's.

       Returns:
           np.ndarray: An image array where each connected component
            of the foreground has been labeled with a unique integer.
       """

        rows, cols = image.shape
        visited = np.zeros_like(image, dtype=bool)
        labels = np.zeros_like(image, dtype=int)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        def is_within_bounds(x, y):
            return 0 <= x < rows and 0 <= y < cols

        def bfs(start_x, start_y, label):
            queue = deque([(start_x, start_y)])
            visited[start_x][start_y] = True
            labels[start_x][start_y] = label
            while queue:
                x, y = queue.popleft()
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if is_within_bounds(nx, ny) and not visited[nx][ny] and image[nx][ny] == 1:
                        queue.append((nx, ny))
                        visited[nx][ny] = True
                        labels[nx][ny] = label

        label_count = 1
        for i in range(rows):
            for j in range(cols):
                if not visited[i][j] and image[i][j] == 1:
                    bfs(i, j, label_count)
                    label_count += 1
        return labels

    @staticmethod
    def get_region_values(image: np.ndarray, points: List[Tuple[int, int]]) -> List[Dict[str, int]]:
        """
        For each specified point, determine the labeled region it belongs to in the image, count the number of pixels
        in that region, and assign a value based on the region's size.

        Args:
            image (np.ndarray): The image array where each value indicates a region.
            points (List[Tuple[int, int]]): List of (x, y) tuples representing points whose regions are to be evaluated.

        Returns:
            List[Dict[str, int]]: A list of dictionaries,
            each containing the 'center' (x, y) of the region and its 'value'.
        """
        region_counts = {}
        values = []
        for x, y in points:
            region_number = image[y, x]
            if region_number not in region_counts:
                region_counts[region_number] = np.sum(image == region_number)
            number_of_pixels = region_counts[region_number]
            value = 5 if number_of_pixels > 4000 else 1
            values.append({
                "center": (x, y),
                "value": value
            })
        return values

    def process_image(self) -> NoReturn:
        """
        Main processing function that orchestrates the sequence of image processing steps:
        reading and processing the image, computing histograms, finding thresholds, segmenting,
        labeling, calculating centroids, and displaying results.

        This method relies on several helper methods to perform these tasks and ultimately visualizes
        the processing results.
        """
        red = np.float32(self.image[:, :, 0])
        green = np.float32(self.image[:, :, 1])
        blue = np.float32(self.image[:, :, 2])
        g = 255 - ((green * 255) / (red + green + blue))
        g_hist = self.compute_smooth_histogram(g, 10)
        threshold = self.find_first_local_minimum(g_hist)
        segmented_image = g.copy()
        segmented_image[segmented_image < threshold] = 0
        segmented_image[segmented_image >= threshold] = 1
        regions = self.label_image_regions(segmented_image)
        points = self.calculate_region_centroids(regions)
        coin_values = self.get_region_values(regions, points)
        self.display_results(self.image, g, g_hist, threshold, segmented_image, regions, points, coin_values)

    @staticmethod
    def display_results(original_img,
                        green_component,
                        green_histogram,
                        threshold,
                        segmented_img,
                        labeled_regions,
                        centers,
                        region_values) -> NoReturn:
        """
        Visualize and display the results of image processing, including the original image, processed channels,
        histograms, segmentation results, and labeled regions.
        Centroids and region values are also displayed on the original image.

        Args:
            original_img (np.ndarray): The original image.
            green_component (np.ndarray): The green channel of the image processed.
            green_histogram (np.ndarray): The histogram of the green channel.
            threshold (int): The threshold value used for segmentation.
            segmented_img (np.ndarray): The binary image resulting from segmentation.
            labeled_regions (np.ndarray): The image with labeled regions.
            centers (List[List[int]]): List of centroids of the regions.
            region_values (List[Dict[str, int]]): List of dictionaries representing the value assigned to each region.
        """
        fig = plt.figure(figsize=(18, 10))
        titles = ['Original Image', 'Green Channel', 'Histogram of Green Channel', 'Segmentation Result',
                  'Labeled Regions', 'Centers of Mass', 'Region Values']

        images = [original_img, green_component, green_histogram, segmented_img, labeled_regions, original_img,
                  original_img]
        for i, (img, title) in enumerate(zip(images, titles), 1):
            ax = fig.add_subplot(2, 4, i)
            if title == 'Histogram of Green Channel':
                ax.plot(img)
                ax.axvline(x=threshold, color='red', label=f'Threshold: {threshold}')
                ax.set_xlim([0, 255])
                ax.set_ylim([0, 255])
                ax.legend()
            else:
                cmap = 'gray' if title in ['Green Channel',
                                           'Segmentation Result'] else 'jet' if title == 'Labeled Regions' else None
                ax.imshow(img, cmap=cmap)
                if title == 'Centers of Mass':
                    ax.scatter([c[0] for c in centers], [c[1] for c in centers], color='red', marker='+')
                elif title == 'Region Values':
                    for coin in region_values:
                        ax.text(coin['center'][0], coin['center'][1], str(coin['value']), color='red', fontsize=12,
                                ha='center')
            ax.set_title(title)
            ax.axis('off')
        plt.tight_layout()
        plt.show()


def main():
    # Usage
    processor = ImageProcessor('./cv07_segmentace.bmp')
    processor.process_image()


if __name__ == "__main__":
    main()

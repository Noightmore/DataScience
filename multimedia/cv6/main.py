import numpy as np
import heapq
from collections import Counter


def rle_encode(data):
    result = []
    buffer = ""
    count = 0

    for char in data:
        if buffer != char:
            if count > 0:
                result.append(count)
                result.append(buffer)
            buffer = char
            count = 1
        else:
            count += 1

    result.append(count)
    result.append(buffer)

    return result


def rle_decode(encoded_data):
    decoded_data = []

    for i in range(0, len(encoded_data), 2):
        count = encoded_data[i]
        char = encoded_data[i + 1]
        decoded_data.append(char * count)

    return "".join(decoded_data)


class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_huffman_tree(data):
    # Count the frequency of each character in the data
    frequency = Counter(data)

    # Create a priority queue of Huffman nodes
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    # Build the Huffman tree
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        parent = HuffmanNode(None, left.frequency + right.frequency)
        parent.left, parent.right = left, right
        heapq.heappush(priority_queue, parent)

    return priority_queue[0]


def build_huffman_codes(root, current_code="", huffman_codes=None):
    if huffman_codes is None:
        huffman_codes = {}

    if root.char is not None:
        huffman_codes[root.char] = current_code
        return

    build_huffman_codes(root.left, current_code + "0", huffman_codes)
    build_huffman_codes(root.right, current_code + "1", huffman_codes)

    return huffman_codes


def huffman_encode(data):
    root = build_huffman_tree(data)
    huffman_codes = build_huffman_codes(root)
    print(huffman_codes)
    encoded_data = "".join(huffman_codes[char] for char in data)
    return encoded_data, root


def huffman_decode(encoded_data, root):
    decoded_data = []
    current = root

    for bit in encoded_data:
        if bit == "0":
            current = current.left
        else:
            current = current.right

        if current.char is not None:
            decoded_data.append(current.char)
            current = root

    return np.array(decoded_data, dtype='uint8')


def main():
    print("RLE")
    with open("./Cv06_RLE_data.bin", "r", encoding="utf-8") as file_handle:
        nums = np.fromfile(file_handle, dtype='uint8')
        # print(nums)
        nums = [str(x) for x in nums]
        print("".join(nums))
        out = rle_encode(nums)
        print(out)

        out2 = rle_decode(out)
        print(out2)

    print("Huffman")

    with open("./Cv05_LZW_data.bin", "r", encoding="utf-8") as file_handle:
        data = np.fromfile(file_handle, dtype='uint8')

        encoded_data, huffman_tree = huffman_encode(data)
        print(f"Original data: {data}")
        print(f"Encoded data: {encoded_data}")

        decoded_data = huffman_decode(encoded_data, huffman_tree)
        print(f"Decoded data:  {decoded_data}")


if __name__ == "__main__":
    main()

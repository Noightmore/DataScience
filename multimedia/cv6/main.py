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

    def __gt__(self, other):
        return self.frequency > other.frequency

    def __eq__(self, other):
        return self.frequency == other.frequency


class HuffmanCoding:

    def __init__(self, data):
        self.data = data
        self.root = None
        self.huffman_codes = None

    # def __str__(self, prefix="", is_left=True):
    #     if self.root:
    #         print(prefix + ("|-- " if is_left else "`-- ") + str(self.root.char) + " (" + str(self.root.freq) + ")")
    #         prefix += "|   " if is_left else "    "
    #         print_huffman_tree(root.left, prefix, True)
    #         print_huffman_tree(root.right, prefix, False)

    def build_huffman_tree(self):
        frequency = Counter(self.data)
        priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(priority_queue)

        # Build the Huffman tree
        while len(priority_queue) > 1:
            left = heapq.heappop(priority_queue)
            right = heapq.heappop(priority_queue)
            parent = HuffmanNode(None, left.frequency + right.frequency)
            parent.left, parent.right = left, right
            heapq.heappush(priority_queue, parent)

        self.root = priority_queue[0]

    def build_huffman_codes(self, root=None, current_code=""):
        if root is None:
            root = self.root
        if self.huffman_codes is None:
            self.huffman_codes = {}

        if root.char is not None:
            self.huffman_codes[root.char] = current_code
            return

        self.build_huffman_codes(root.left, current_code + "0")
        self.build_huffman_codes(root.right, current_code + "1")

    def huffman_encode(self):
        self.build_huffman_tree()
        self.build_huffman_codes()
        encoded_data = "".join(self.huffman_codes[char] for char in self.data)
        return encoded_data

    def huffman_decode(self, encoded_data):
        decoded_data = []
        current = self.root

        for bit in encoded_data:
            if bit == "0":
                current = current.left
            else:
                current = current.right

            if current.char is not None:
                decoded_data.append(current.char)
                current = self.root

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

    print()
    print("Huffman")

    with open("./Cv05_LZW_data.bin", "r", encoding="utf-8") as file_handle:
        data = np.fromfile(file_handle, dtype='uint8')

        huffman_coding = HuffmanCoding(data)

        print(np.array(data, dtype='uint8'))
        encoded_data = huffman_coding.huffman_encode()
        print(encoded_data)
        decoded_data = huffman_coding.huffman_decode(encoded_data)
        print(decoded_data)

        #print(str(huffman_coding))


if __name__ == "__main__":
    main()

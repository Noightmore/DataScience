"""Funkce řešící cvičení 5 z MT

Raises:
    LookupError: Pokud není fráze nalezena ve slovníku
"""
import numpy as np


class LZW:
    """
        Třída pro provedení LZW komprese a dekomprese nad daty
    """

    def __init__(self, data: list[str]) -> None:
        self.data = data
        self.ratio = 0
        self.alphabet = {v: str(k + 1) for k, v in enumerate(sorted(list(set(data))))}
        self.max_iters = 1000

    def compress(self):
        dictionary = {chr(i): i for i in range(256)}
        max_code = 255
        result = []
        current_code = ""

        for symbol in self.data:
            current_code += symbol
            if current_code not in dictionary:
                dictionary[current_code] = max_code + 1
                max_code += 1
                result.append(dictionary[current_code[:-1]])
                current_code = symbol

        result.append(dictionary[current_code])
        self.data = result

    def decompress(self):
        dictionary = {i: chr(i) for i in range(256)}
        result = []
        current_code = [self.data[0]]
        result.append(dictionary[self.data[0]])
        next_code = 256

        for code in self.data[1:]:
            if code in dictionary:
                current_code.append(code)
            else:
                new_phrase = current_code + [current_code[0]]
                dictionary[next_code] = ''.join(new_phrase)
                next_code += 1
                result.append(dictionary[code])
                current_code = [code]

        self.data = result


def main():
    with open("./Cv05_LZW_data.bin", "r", encoding="utf-8") as file_handle:
        integers = np.fromfile(file_handle, dtype='uint8')

        test_suites = {
            "Příklad z přednášky": ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'b', 'c', 'b', 'a'],
            "Binární data": [str(x) for x in integers]
        }

        for key, value in test_suites.items():
            driver = LZW(value)

            # Original data
            original_data = "".join(driver.data)

            # Compression
            driver.compress()
            #compressed_data = "".join(driver.data)
            print(driver.data)

            # Decompression
            driver.decompress()
            #decompressed_data = "".join(driver.data)
            print(driver.data)

            # Check for data loss
            #data_loss = original_data == decompressed_data

            #print(f"Label: {key}")
            #print(f"Original Data: {original_data}")
            #print(f"Compressed Data: {compressed_data}")
            #print(f"Decompressed Data: {decompressed_data}")
            #print(f"Data Loss: {data_loss}\n")


if __name__ == "__main__":
    main()

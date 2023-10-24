import numpy as np


def lzw_compress(data: list[str], max_iters: int = 1000) -> list[str]:

    phrases = {v: str(k + 1) for k, v in enumerate(sorted(list(set(data))))}
    remainder = data.copy()
    iteration = 0
    result = []

    while len(remainder) > 0 and iteration < max_iters:
        iteration += 1
        longest_phrase = remainder
        longest_phrase_str = "".join(longest_phrase)

        while longest_phrase_str not in phrases:
            longest_phrase = longest_phrase[:-1]
            longest_phrase_str = "".join(longest_phrase)

        result.append(phrases[longest_phrase_str])
        new_phrase = "".join(remainder[0:len(longest_phrase) + 1])
        new_phrase_index = len(phrases.items())
        phrases[new_phrase] = str(new_phrase_index + 1)
        remainder = remainder[len(longest_phrase):]

    return result


def lzw_decompress(data: list[str], og_data: list[str], max_iters: int = 1000) -> list[str]:

    phrases = {v: k for k, v in {v: str(k + 1) for k, v in enumerate(sorted(list(set(og_data))))}.items()}
    remainder = data.copy()
    iteration = 0
    result = []

    while len(remainder) > 0 and iteration < max_iters:
        iteration += 1
        encoded_symbol = remainder[0]

        if encoded_symbol in phrases:
            result.append(phrases[encoded_symbol])

            if len(result) > 1:
                new_phrase_index = str(len(phrases.items()) + 1)
                phrases[new_phrase_index] = result[-2] + result[-1][0]

        else:
            if len(result) > 0:
                new_phrase_index = len(phrases.items()) + 1
                nwe_phrase = result[-1] + result[-1][0]
                phrases[new_phrase_index] = nwe_phrase
                result.append(nwe_phrase)

        remainder = remainder[1:]

    return result


def main():
    # load ./Cv05_LZW_data.bin as raw binary data
    with open("./Cv05_LZW_data.bin", "r", encoding="utf-8") as file_handle:
        nums = np.fromfile(file_handle, dtype='uint8')

        # convert to list of strings
        data = [str(x) for x in nums]
        print("".join(data))
        compressed_data = lzw_compress(data)
        print(compressed_data)

        decompressed_data = lzw_decompress(compressed_data, data)
        print("".join(decompressed_data))


if __name__ == "__main__":
    main()

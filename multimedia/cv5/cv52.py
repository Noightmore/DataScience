import numpy as np


def lzw_encode(data):
    dictionary = {chr(i): i for i in range(256)}
    current_code = 256

    result = []
    buffer = ""

    for char in data:
        buffer += char
        if buffer not in dictionary:
            dictionary[buffer] = current_code
            current_code += 1
            result.append(dictionary[buffer[:-1]])
            buffer = char

    result.append(dictionary[buffer])

    return result


def lzw_decode(encoded_data):
    dictionary = {i: chr(i) for i in range(256)}
    current_code = 256

    decoded_data = [chr(encoded_data[0])]
    buffer = chr(encoded_data[0])

    for code in encoded_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == current_code:
            entry = buffer + buffer[0]
        else:
            raise ValueError("Decoding error: Code not found in dictionary.")

        decoded_data.append(entry)
        dictionary[current_code] = buffer + entry[0]
        current_code += 1
        buffer = entry

    return "".join(decoded_data)


def main():
    with open("./Cv05_LZW_data.bin", "r", encoding="utf-8") as file_handle:
        nums = np.fromfile(file_handle, dtype='uint8')

        #print(nums)
        nums = [str(x) for x in nums]
        print("".join(nums))
        out = lzw_encode(nums)
        # convert out to string
        out2 = [str(x) for x in out]
        print(out2)
        print(lzw_decode(out))


if __name__ == "__main__":
    main()

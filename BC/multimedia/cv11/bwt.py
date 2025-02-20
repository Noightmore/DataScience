from collections import deque
from typing import Tuple, List


def bwt(text: str) -> tuple[str, int, list[str]]:
    """Burrows-Wheeler transform of input string."""

    block_size = len(text)
    encoding_matrix = [text] * block_size

    for i, x in enumerate(encoding_matrix):
        queue = deque(x)
        queue.rotate(i)
        encoding_matrix[i] = str.join("", queue)

    encoding_matrix = sorted(encoding_matrix)
    encoded_output = str.join("", [x[-1] for x in encoding_matrix])
    input_index = encoding_matrix.index(text)

    return encoded_output, input_index, encoding_matrix


def ibwt(encoded_text: str, input_index: int) -> tuple[str, list[str]]:
    """Inverse Burrows-Wheeler transform."""

    decoding_matrix = list(encoded_text)
    for i in range(len(encoded_text) - 1):
        letters_to_add = [x[-1] for x in sorted(decoding_matrix)]
        decoding_matrix = [x + y for x, y in zip(decoding_matrix, letters_to_add)]

    decoding_matrix = sorted(decoding_matrix)
    decoded_output = decoding_matrix[input_index]

    return decoded_output, decoding_matrix


# Example usage
if __name__ == "__main__":
    input_text = "hello world"
    out = bwt(input_text)
    print(f"Original: {input_text}")
    print(f"BWT: {out[0]}")
    print(f"BWT encoding matrix: {out[2]}")
    print()
    print(f"IBWT: {ibwt(out[0], out[1])}")
    print(f"IBWT decoding matrix: {ibwt(out[0], out[1])[1]}")

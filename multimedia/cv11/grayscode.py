
def from_binary_to_gray(binary):
    """Converts binary number to Gray code."""
    gray = binary[0]
    for i in range(1, len(binary)):
        gray += str(int(binary[i - 1]) ^ int(binary[i]))
    return gray


def from_gray_to_binary(gray):
    """Converts Gray code to binary number."""
    binary = gray[0]
    for i in range(1, len(gray)):
        binary += str(int(binary[i - 1]) ^ int(gray[i]))
    return binary


def main():
    my_number = 123

    binary = bin(my_number)[2:]
    gray = from_binary_to_gray(binary)
    print('Binary number: {}\nGray code: {}'.format(binary, gray))
    print()
    print()

    binary = from_gray_to_binary(gray)
    binary = int(binary, 2)
    print('Gray code: {}\nBinary number: {}'.format(gray, binary))


if __name__ == '__main__':
    main()

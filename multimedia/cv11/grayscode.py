def from_binary_to_gray(binary):
    """Converts binary number to Gray code."""
    gray = binary ^ (binary >> 1)
    return gray


def from_gray_to_binary(gray):
    """Converts Gray code to binary number."""
    binary = gray
    while gray >> 1:
        gray >>= 1
        binary ^= gray
    return binary


def main():
    my_number = 123

    binary = my_number
    gray = from_binary_to_gray(binary)
    print('Decimal number: {}\nGray code: {}'.format(binary, gray))
    print()

    binary = from_gray_to_binary(gray)
    print('Gray code: {}\nDecimal number: {}'.format(gray, binary))


if __name__ == '__main__':
    main()

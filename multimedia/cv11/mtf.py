from typing import Tuple


def encode_mtf(text: str, alphabet: list[str]) -> tuple[str, str]:
    encoding_stack = alphabet.copy()
    encoded_output = []

    for character in list(text):
        if character not in encoding_stack:
            message = f"Znak '{character}' není v povolené abecedě"
            raise LookupError(message)

        index = encoding_stack.index(character)
        encoded_output.append(str(index))

        encoding_stack.remove(character)
        encoding_stack.insert(0, character)

    return str.join(", ", encoded_output), str.join("", encoding_stack)


def decode_mtf(encoded_text: str, alphabet: list[str]) -> tuple[str, str]:

    #if not encoded_text.isdigit():
     #   raise ValueError("Encoded text must be a string of digits.")

    decoding_stack = alphabet.copy()
    decoded_output = []

    for index in encoded_text.split(", "):
        character = decoding_stack[int(index)]
        decoded_output.append(character)

        decoding_stack.remove(character)
        decoding_stack.insert(0, character)

    return str.join("", decoded_output), str.join("", decoding_stack)


def main():
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    user_input = input("text for MTF: ")

    encoded_output, encoding_stack = encode_mtf(user_input, alphabet)


    print()
    print(f"Input: {user_input}")
    print(f"Abeceda: {str.join('', alphabet)}")
    print()
    print(f"Kódování: {encoded_output}")
    print(f"Kódovací zásobník: {encoding_stack}")
    print()

    decoded_output, decoding_stack = decode_mtf(encoded_output, alphabet)

    print(f"Dekódování: {decoded_output}")
    print(f"Dekódovací zásobník: {decoding_stack}")
    print()


if __name__ == "__main__":
    main()

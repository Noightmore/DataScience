"""
Vytvorte funkce encrypt a decrypt pro Caesarovu sifru.
Kompletni zadani v elearningu.
"""


def encrypt(text, offset):
    """

    :param text: input text a-z, A-Z, space
    :param offset: amount of characters to shift to the right in the alphabet
    :return:
    """
    encrypted_chars = []
    for character in text:
        if character == " ":
            encrypted_chars.append(" ")
        elif character.isupper():
            encrypted_chars.append(chr((ord(character) + offset - 65) % 26 + 65).upper())
        else:
            encrypted_chars.append(chr((ord(character) + offset - 97) % 26 + 97).lower())

    return "".join(encrypted_chars)


def decrypt(text, offset):
    """

    :param text: input text a-z, A-Z, space
    :param offset: amount of characters to shift to the left in the alphabet
    :return:
    """
    decrypted_chars = []
    for character in text:
        if character == " ":
            decrypted_chars.append(" ")
        elif character.isupper():
            decrypted_chars.append(chr((ord(character) - offset - 65) % 26 + 65).upper())
        else:
            decrypted_chars.append(chr((ord(character) - offset - 97) % 26 + 97).lower())

    return "".join(decrypted_chars)

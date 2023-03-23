def encrypt(text, key):

    # Convert the text to a list of characters
    chars = list(text)
    # Encrypt each character
    encrypted_chars = [chr((ord(c) + key) % 256) for c in chars]
    # Convert the encrypted characters back to a string
    encrypted_text = "".join(encrypted_chars)
    # Return the encrypted text and the key
    return encrypted_text


def decrypt(encrypted_text, key):
    # Convert the encrypted text to a list of characters
    encrypted_chars = list(encrypted_text)
    # Decrypt each character
    decrypted_chars = [chr((ord(c) - key) % 256) for c in encrypted_chars]
    # Convert the decrypted characters back to a string
    decrypted_text = "".join(decrypted_chars)
    # Return the decrypted text
    return decrypted_text



def decrypt_vigenere_bruteforce_with_words(encrypted_text, known_words, max_key_length=10):
    decrypted_texts = {}

    for key_length in range(1, max_key_length + 1):
        possible_keys = [''.join(chr((ord('A') + i) % 26) for i in range(key_length))]
        for i in range(1, key_length):
            possible_keys.append(possible_keys[0][-i:] + possible_keys[0][:-i])

        for key in possible_keys:
            decrypted_text = decrypt_vigenere_cipher(encrypted_text, key)

            # Check if known words are present in the decrypted text
            if all(word.lower() in decrypted_text.lower() for word in known_words):
                decrypted_texts[(key, key_length)] = decrypted_text

    return decrypted_texts

# Example usage with your encrypted text
text1 = "TEWFYWYNKUCOMOWOJTEWFYWYNKUCOMOWOJOWOJKXCKBUKDOTYDKNOVRYZKXYDTKBIUCWOJDOFUKBKTOCSFUCONKCFRMKXSVKUCYZSWECIBYLRMKXSMEVYZSMERKNYFTEWFYWYNONUTEWFYWYNONU"

# Known words
known_words = ["domov", "roads"]

# Attempt to decrypt using Vigenere cipher brute-force
decrypted_texts1 = decrypt_vigenere_bruteforce_with_words(text1, known_words)

# Display the results
print("Decrypted Texts 1:")
for key_info, decrypted_text in decrypted_texts1.items():
    print(f"Key: {key_info[0]}, Key Length: {key_info[1]}, Decrypted Text: {decrypted_text}")

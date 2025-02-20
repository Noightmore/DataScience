from numpy import random


def is_prime(num):
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(num ** 0.5), 2):
        if num % i == 0:
            return False
    return True


def generate_random_prime(min, max):
    while True:
        num = random.randint(min, max)
        if is_prime(num):
            return num


def rsa_encrypt_decrypt(message, p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    print(phi)

    e = 0
    while e == 0:
        e = random.randint(2, phi)
        if e % 2 == 0:
            e = 0

    print("e is: ", e)

    try:
        d = pow(e, -1, phi)
    except ValueError:

        print("e and phi are not coprime")

        return

    print("d is: ", d)

    # convert message to array of ints
    message = [ord(i) for i in str(message)]

    print("Message is: ", message)

    # encrypt
    encrypted_message = []
    for i in message:
        encrypted_message.append(pow(i, e, n))

    print("Encrypted message is: ", encrypted_message)

    # decrypt
    decrypted_message = []
    for i in encrypted_message:
        decrypted_message.append(pow(i, d, n))

    print("Decrypted message is: ", decrypted_message)

    # convert decrypted message to string
    decrypted_message = [chr(i) for i in decrypted_message]
    decrypted_message = "".join(decrypted_message)
    print("Decrypted message is: ", decrypted_message)


def main():
    print("Generating random prime numbers...")
    p = generate_random_prime(1000, 10000)
    q = generate_random_prime(1000, 10000)

    print("p is: ", p)
    print("q is: ", q)

    #message = "Hello world!"
    message = input("Enter a message: ")

    rsa_encrypt_decrypt(message, p, q)


if __name__ == "__main__":
    main()

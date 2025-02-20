/*
#include <stdlib.h>
#include <stdio.h>
#include <gmp.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

unsigned long long power(unsigned long long base, unsigned long long exponent) {
    unsigned long long result = 1;
    while (exponent > 0) {
        if (exponent % 2 == 1) {
            result *= base;
        }
        base *= base;
        exponent /= 2;
    }
    return result;
}


bool isPrime(int num) {
    if (num <= 1) {
        return false;
    }
    for (int i = 2; i * i <= num; ++i) {
        if (num % i == 0) {
            return false;
        }
    }
    return true;
}


unsigned long long generate_random_prime_number(int min, int max)
{
    int randomNum;
    do {
        randomNum = rand() % (max - min + 1) + min;
    } while (!isPrime(randomNum));

    return randomNum;
}


unsigned long long rsa_encrypt(unsigned long message, unsigned long long p, unsigned long q)
{
    unsigned long n = p * q;
    // euler function - random prime numbers
    unsigned long upper_bound = (p - 1) * (q - 1);
    unsigned long e = 0;

    // pick random number between 1 and upper_bound
    while (e == 0)
    {
        e = rand() % upper_bound + 1;
        if (e % 2 == 0)
        {
            e = 0;
        }
    }

    long d = 0;

    // find d
    for (int i = 1; i < upper_bound; i++)
    {
        if ((e * i) % upper_bound == 1)
        {
            d = i;
            break;
        }
    }

    printf("n: %ld\n", n);
    printf("e: %ld\n", e);
    printf("d: %ld\n", d);

    */
/*mpz_t base, result, mz_e, mz_d, mz_n;
    mpz_init(base);
    mpz_init(result);
    mpz_init(mz_e);
    mpz_init(mz_d);
    mpz_init(mz_n);

    mpz_set_ui(mz_e, e);
    mpz_set_ui(mz_d, d);
    mpz_set_ui(mz_n, n);

    mpz_set_ui(base, message);

    mpz_pow_ui(result, base, (unsigned long) mz_e);

    mpz_mod(result, result, mz_n);*//*


    //printf("Encrypted message: %llu\n", encrypted_message);

    unsigned long long encrypted_message = power(message, e) % n;

    unsigned long long decrypted_message = power(encrypted_message, d) % n;

    //printf("Decrypted message: %llu\n", decrypted_message);
    //printf("Decrypted message: %c\n", (char) decrypted_message + 48);

    return encrypted_message;

}

unsigned long long rsa_decrypt(unsigned long long message, unsigned long long p, unsigned long long q)
{
    unsigned long n = p * q;
    // euler function - random prime numbers
    unsigned long upper_bound = (p - 1) * (q - 1);
    unsigned long e = 0;

    // pick random number between 1 and upper_bound
    while (e == 0)
    {
        e = rand() % upper_bound + 1;
        if (e % 2 == 0)
        {
            e = 0;
        }
    }

    long d = 0;

    // find d
    for (int i = 1; i < upper_bound; i++)
    {
        if ((e * i) % upper_bound == 1)
        {
            d = i;
            break;
        }
    }

   printf("n: %ld\n", n);
    printf("e: %ld\n", e);
   printf("d: %ld\n", d);


    unsigned long long decrypted_message = power(message, d) % n;

    //printf("Decrypted message: %llu\n", decrypted_message);
    //printf("Decrypted message: %c\n", (char) decrypted_message + 48);

    return decrypted_message;

}


int main_bruh()
{
    // konsole app

    printf("RSA encryption\n");
    printf("Enter message to encrypt: ");
    char input[256];
    memset(input, 0, 256);

    fgets(input, 256, stdin);

    //printf("Input: %s\n", input);

    // remove newline character
    input[strlen(input) - 1] = '\0';
    unsigned long long p = generate_random_prime_number(1000, 10000);
    unsigned long long q = generate_random_prime_number(1000, 10000);

    printf("p: %llu\n", p);
    printf("q: %llu\n", q);

    unsigned long long encrypted_message_buff[256];
    memset(encrypted_message_buff, 0, 256);

    for (int i = 0; i < strlen(input); i++)
    {
        encrypted_message_buff[i] = rsa_encrypt((long) (input[i] - 48), 3, 11);
    }

    printf("Encrypted message: ");
    for (int i = 0; i < strlen(input); i++)
    {
        printf("%llu ", encrypted_message_buff[i]);
    }

    printf("Decrypted message: ");
    for (int i = 0; i < strlen(input); i++)
    {
        printf("%c", (char) rsa_decrypt(encrypted_message_buff[i], 3, 11) + 48);
    }

    return 0;
}*/

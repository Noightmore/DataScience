/*
#include <stdlib.h>
#include <stdio.h>
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


void rsa_encrypt_and_decrypt(char* message, unsigned long long p, unsigned long q)
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

    // find d
    unsigned long long d = 0;

    // check if d is valid
    while (d * e % upper_bound != 1)
    {
        d = rand() % upper_bound + 1;
        if (d % 2 == 0)
        {
            d = 0;
        }
    }

    unsigned long long encrypted_message[strlen(message)];
    memset(encrypted_message, 0, sizeof(encrypted_message));

    for(int i = 0; i < strlen(message); i++)
    {
        printf("%d\n", message[i] - 48);
        encrypted_message[i] = power(message[i] - 48, e) % n;
        //printf("%llu\n", encrypted_message[i] - 48);
    }

    // print encrypted message
    printf("Encrypted message: ");
    for(int i = 0; i < strlen(message); i++)
    {
        printf("%llu ", encrypted_message[i]);
    }

    printf("\n");

    // decrypt message
    unsigned long long decrypted_message[strlen(message)];
    memset(decrypted_message, 0, sizeof(decrypted_message));

    for(int i = 0; i < strlen(message); i++)
    {
        decrypted_message[i] = power(encrypted_message[i], d) % n;
    }

    // print decrypted message
    printf("Decrypted message: ");
    for(int i = 0; i < strlen(message); i++)
    {
        printf("%llu ", decrypted_message[i]);
        printf("%c ", (char) decrypted_message[i] + 48);
    }
}


int main()
{
    //srand(time(NULL));
    char message[100];
    printf("Enter a message: ");
    fgets(message, 100, stdin);

    // remove newline character
    message[strlen(message) - 1] = '\0';


    unsigned long long p = generate_random_prime_number(1000, 10000);
    unsigned long long q = generate_random_prime_number(1000, 10000);

    printf("p: %llu\n", p);
    printf("q: %llu\n", q);

    rsa_encrypt_and_decrypt(message, 3, 11);

    return 0;
}*/

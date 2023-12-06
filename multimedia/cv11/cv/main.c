#include <stdio.h>

#define XOR(a,b) (a ^ b)

typedef unsigned char uint8_t; // 8 bits

typedef struct signal
{
    uint8_t number;
    uint8_t complement;
} signal;


int repairSignal(signal *s);
void printBinary(unsigned char num);


int main()
{

        // signal s1 = 160, 223
        // test signal:
        //signal s1 = {0b000000011, 0b000001011};
        signal signals[3] = {
                {160, 223},
                {64, 65},
                {128, 126}
        };

        for (int i = 0; i < 3; i++)
        {
                printf("Signal %d: ", i);
                printBinary(signals[i].number);
                printf("Complement: ");
                printBinary(signals[i].complement);
                repairSignal(&signals[i]);
                printf("\n");
        }

        return 0;
}

int repairSignal(signal *s)
{
        // count the number of 0s in the number
        int numZeros = 0;
        for (int i = 0; i < 8; i++)
        {
                if (((s->number >> i) & 1) == 0)
                {
                        numZeros++;
                }
        }

        printf("numZeros: %d\n", numZeros);

        int isOdd = (numZeros % 2 != 0);

        if (isOdd)
        {
                // invert the complement
                s->complement = XOR(s->complement, 255);
        }

        // check if the signal is correct
        if (XOR(s->number, s->complement) != 255)
        {
                uint8_t error_bit_pos = XOR(s->number, s->complement);
                printf("Error bit position: ");

                // count the number of 0s in the error bit position
                int numOnes = 0;
                for (int i = 0; i < 8; i++)
                {
                        if (((error_bit_pos >> i) & 1) == 1)
                        {
                                numOnes++;
                        }
                }

                if (numOnes > 1)
                {
                        // invert the error bit position
                        error_bit_pos = XOR(error_bit_pos, 255);
                }

                printBinary(error_bit_pos);

                // flip the error bit
                uint8_t correction = XOR(s->number, error_bit_pos);
                ///printf("Correction: ");
                printBinary(correction);
                printf("Corrected signal: %d", correction);

        }

        return 0; // success

}

void printBinary(unsigned char num)
{
        // Determine the number of bits in an unsigned char
        int numBits = sizeof(num) * 8;

        // Iterate through each bit and print it
        for (int i = numBits - 1; i >= 0; i--)
        {
                // Use bitwise AND to check the value of the current bit
                int bit = (num >> i) & 1;
                printf("%d", bit);

                // Add space for better readability (optional)
                if (i % 4 == 0)
                {
                        printf(" ");
                }
        }

        printf("\n");
}


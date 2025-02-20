from collections import Counter
import numpy as np
from is_even import is_even as ie


def repair_inverse_code(number_list, compliment_list):
    #  count the number of 0s in the binary representation of the number

    for number, compliment in zip(number_list, compliment_list):
        binary = bin(number)[2:]
        binary = binary.zfill(8)
        binary = list(binary)

        binary_compliment = bin(compliment)[2:]
        binary_compliment = binary_compliment.zfill(8)
        binary_compliment = list(binary_compliment)

        #print(binary)

        # count number of 0s in binary compliment
        count = Counter(binary)

        # if binary has odd count of zeros the invert the compliment

        was_inversed = (ie.is_even(count['0']))

        if was_inversed:
            print("Odd number of zeros")
            # binary not
            compliment = ~compliment
            #print("Compliment is now: ", compliment)

        else:
            print("Even number of zeros")
            #print("Compliment is now: ", compliment)



        # is there a mistake?
        if xor(number, compliment) == 0:
            print("No mistake")
            print("Number is: ", number)
            print("Compliment is: ", compliment)
        else:
            print("Mistake")
            print("Number is: ", number)
            print("Compliment is: ", compliment)

            # learn the xor result and the position of the flipped bit
            xor_result = xor(number, compliment)
            res = xor(xor_result, xor_result)

            # flip the bit at the position of the xor result in the number
            # and print the result
            print("Flipped bit at position: ", xor_result)
            # correct the number at the position of the xor result
            # convert the number to binary
            binary = bin(number)[2:]
            binary = binary.zfill(8)
            binary = list(binary)

            # convert the xor result to binary
            xor_binary = bin(~res)[2:]
            xor_binary = xor_binary.zfill(8)
            xor_binary = list(xor_binary)

            print("Binary is: ", binary)
            print("Xor binary is: ", xor_binary)

            print(number | res)


if __name__ == "__main__":
    xor = lambda x, y: x ^ y


    number_list = np.array([160, 64, 128], dtype="uint8")
    compliment_list = np.array([223, 65, 126], dtype="uint8")

    repair_inverse_code(number_list, compliment_list)

from collections import Counter
import random
from is_even import is_even as ie


def flip_random_bit(number):
    # Convert the number to binary representation without the '0b' prefix
    binary_representation = bin(number)[2:]

    # Choose a random position to flip a bit
    flip_position = random.randint(0, len(binary_representation) - 1)

    # Flip the bit at the chosen position
    flipped_binary = list(binary_representation)
    flipped_binary[flip_position] = '1' if flipped_binary[flip_position] == '0' else '0'

    # Convert the binary representation back to an integer
    flipped_number = int(''.join(['0b'] + flipped_binary), 2)

    return flipped_number


def repair_inverse_code(number, compliment):
    xor = lambda a, b: a ^ b

    # 1. Convert number to binary
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

    if not (ie.is_even(count['0'])):
        print("Odd number of zeros")
        # binary not

        #print("Compliment is now: ", compliment)

    else:
        print("Even number of zeros")
        compliment = ~compliment
        #print("Compliment is now: ", compliment)

    # xor the compliment and the number
    # if the result is 0 then the number is correct

    # is there a mistake?
    if xor(number, compliment) == 0:
        print("No mistake")
        print("Number is: ", number)
        print("Compliment is: ", compliment)

    else:
        errors = []

        data_fixed = binary.copy()
        safety_fixed = binary_compliment.copy()

        for i in range(0, len(binary)):
            data_char = binary[i]
            safety_char = binary_compliment[i]
            fixed_char = xor(int(data_char), int(safety_char))

            errors.append(str(fixed_char))

        test = {v:k for k, v in Counter(errors).items()}
        error_character = test[1]
        error_index = errors.index(str(error_character))

        if error_character == "1":
            safety_fixed[error_index] = abs(1 - int(safety_fixed[error_index]))
        else:
            data_fixed[error_index] = abs(1 - int(data_fixed[error_index]))

        # convert data_fixed to int
       # join all the characters in the list to a string and then convert the string to an integer with base 2
        data_fixed = int("".join(map(str, data_fixed)), 2)
        print("Number is: ", data_fixed)


def exchange_numbers_with_flip(num, compliment):
    if random.randint(0, 1) == 0:
        compliment_received = flip_random_bit(compliment)
        num_received = num
        print("Compliment was flipped")
    else:
        num_received = flip_random_bit(num)
        compliment_received = compliment
        print("Number was flipped")

    return num_received, compliment_received


def main():
    # Test Case 1
    num1 = 160
    compliment1 = 223
    print("Unchanged number")
    print(f"Original Number: {num1}, Original Compliment: {compliment1}")
    repair_inverse_code(num1, compliment1)
    print("--------------------")

    num1 = 64
    compliment1 = 65
    print("Unchanged number")
    print(f"Original Number: {num1}, Original Compliment: {compliment1}")
    repair_inverse_code(num1, compliment1)
    print("--------------------")

    num1 = 128
    compliment1 = 126
    print("Unchanged number")
    print(f"Original Number: {num1}, Original Compliment: {compliment1}")
    repair_inverse_code(num1, compliment1)
    print("--------------------")

    # print("Flipped number")
    # num_received1, compliment_received1 = exchange_numbers_with_flip(num1, compliment1)
    # print(f"Received Number : {num_received1}, Received Compliment: {compliment_received1}")
    # repair_inverse_code(num_received1, compliment_received1)
    # print()

    # # Test Case 2
    # print("Unchanged number")
    # num2 = random.randint(0, 100)
    # compliment2 = num2 if random.randint(0, 1) == 0 else ~num2
    # print(f"Original Number: {num2}, Original Compliment: {compliment2}")
    # repair_inverse_code(num2, compliment2)
    # print("--------------------")
    #
    # print("Flipped number")
    # num_received2, compliment_received2 = exchange_numbers_with_flip(num2, compliment2)
    # print(f"Received Number : {num_received2}, Received Compliment: {compliment_received2}")
    # repair_inverse_code(num_received2, compliment_received2)
    # print()


if __name__ == "__main__":
    main()


def polynomial_division(dividend, divisor, set_type):
    """
    inputs as [1,2,3] for x^2 + 2x + 3
    coefficients of dividend and divisor
    set types as 'Z', 'Q', 'R', 'C' with the added option to specify the set: Z5, Z7, etc.
    returns quotient and remainder as lists of coefficients
    """

    def stabilize(coeffs, set_type):
        if set_type.startswith('Z'):
            mod = int(set_type[1:]) if len(set_type) > 1 else None

            # we substract or add the modulus to ensure coefficients are within the range
            # depends on whether each coeff is negative or positive
            # since mod in python works as expected:
            # x = -7
            # x % 5
            # Out[3]: 3
            # thi is enough:
            coeffs = [c % mod for c in coeffs] if mod is not None else coeffs

        return coeffs

    def poly_to_string(coeffs):
        """Formats polynomial as a string for nice printing."""
        terms = []
        degree = len(coeffs) - 1
        for i, c in enumerate(coeffs):
            power = degree - i
            if c == 0:
                continue
            term = ""
            if c != 1 or power == 0:
                term += f"{c}"
            if power > 0:
                term += "x"
            if power > 1:
                term += f"^{power}"
            terms.append(term)
        return " + ".join(terms) if terms else "0"

    # Ensure the divisor is not zero
    if not divisor or all(c == 0 for c in divisor):
        raise ValueError("Divisor cannot be zero.")

    # Ensure the dividend is not zero
    if not dividend or all(c == 0 for c in dividend):
        return [], dividend  # If dividend is zero, return empty quotient and original dividend as remainder

    # the division itself
    # Stabilize dividend and divisor before starting
    dividend = stabilize(dividend, set_type)
    divisor = stabilize(divisor, set_type)

    print(f"\nStarting division:")
    print(f"Dividend: {poly_to_string(dividend)}")
    print(f"Divisor:  {poly_to_string(divisor)}\n")

    # Reverse to make polynomial order natural for easier index math
    dividend = dividend[::-1]
    divisor = divisor[::-1]

    remainder = dividend[:]
    quotient = []

    divisor_degree = len(divisor) - 1
    divisor_leading_coeff = divisor[-1]

    while len(remainder) >= len(divisor):
        remainder_leading_coeff = remainder[-1]

        if set_type.startswith('Z') and len(set_type) > 1:
            mod = int(set_type[1:])
            inverse = pow(divisor_leading_coeff, -1, mod)
            leading_term = (remainder_leading_coeff * inverse) % mod
        else:
            leading_term = remainder_leading_coeff / divisor_leading_coeff

        quotient.insert(0, leading_term)

        for i in range(len(divisor)):
            idx = len(remainder) - len(divisor) + i
            remainder[idx] -= leading_term * divisor[i]
            if set_type.startswith('Z') and len(set_type) > 1:
                remainder[idx] %= mod

        while remainder and remainder[-1] == 0:
            remainder.pop()

        print(f"Division step:")
        print(f"  Quotient: {poly_to_string(quotient)}")
        print(f"  Remainder: {poly_to_string(remainder)}\n")

    remainder = remainder[::-1]

    print(f"Final result:")
    print(f"  Quotient: {poly_to_string(quotient)}")
    print(f"  Remainder: {poly_to_string(remainder)}\n")

    return quotient, remainder



def main():
    # Example usage
    dividend = [3, 12, 7, 4]  # Represents 3*x^3 + 12*x^2 + 7*x + 4
    divisor = [1, 1]      # Represents x + 1
    set_type = 'Z5'       # Set type can be 'Z', 'Q', 'R', 'C', or 'Z5', 'Z7', etc.

    quotient, remainder = polynomial_division(dividend, divisor, set_type)
    #print(f"Quotient: {quotient}, Remainder: {remainder}")


if __name__ == "__main__":
    main()

# TD: OVERIT FUNKCIONALITU DLE VYPOCTU NA PAPIR

# TD: dodelat gcd polynomu, nsd, mozna i pekny vypis
# ireducibilia, monicke polynomy


# ehehee, uz nemusime delat, tul restart gang!
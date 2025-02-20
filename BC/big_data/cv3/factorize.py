def prime_factorization(n):
    """
    Returns a list of prime factors of n.
    """
    factors = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)

    factors.sort(reverse=False)
    return factors


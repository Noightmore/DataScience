def compute_pythagorean_theorem(a, b):
    """
    Compute the length of the hypotenuse of a right triangle.

    Args:
        a (float): The length of the first side.
        b (float): The length of the second side.

    Returns:
        float: The length of the hypotenuse.
    """
    return (a ** 2 + b ** 2) ** 0.5


def main():
    c = compute_pythagorean_theorem(3, 4)
    print(c)


if __name__ == "__main__":
    main()

#%%

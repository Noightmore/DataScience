""" program that checks if the triangle is right-angled """


def triangle(side_a, side_b, side_c) -> bool:
    """
    method that check if the triangle is right-angled
    :param side_a:
    :param side_b:
    :param side_c:
    :return:
    """

    return side_a**2 + side_b**2 == side_c**2


def main():
    """
    main method
    """
    is_right_angled = triangle(3, 4, 5)
    print(is_right_angled)


if __name__ == "__main__":
    main()

#%%

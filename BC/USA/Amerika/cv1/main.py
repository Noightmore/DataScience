# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# implement function that computes binomial coefficient (supports very huge numbers)
def compute_binomial_coefficient(n, k):
    if k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return compute_binomial_coefficient(n - 1, k - 1) + compute_binomial_coefficient(n - 1, k)


def get_factorial(n):
    if n == 0:
        return 1
    return n * get_factorial(n - 1)


def main():
    val = get_factorial(9)
    return str(val)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ret = main()
    print(ret)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

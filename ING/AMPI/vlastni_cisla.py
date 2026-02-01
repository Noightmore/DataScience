# matrix 3x3 with random Z vals
import sympy as sp
import random
import numpy as np

def generate_random_integer_matrix(rows, cols, low=-10, high=10):
    return sp.Matrix([[random.randint(low, high) for _ in range(cols)] for _ in range(rows)])

def main():
    A = generate_random_integer_matrix(3, 3)
    print("Generated Matrix A:\n", A)

    # eigenvalues and eigenvectors
    eigen_data = A.eigenvects()
    for eigenval, multiplicity, eigenvecs in eigen_data:
        print(f"Eigenvalue: {eigenval}, Multiplicity: {multiplicity}")
        for vec in eigenvecs:
            print(f"Eigenvector: {vec}")


def prikladek():
    # (5 2 -3)
    # (4 5 -4)
    # (6 4 -4)

    A = sp.Matrix([[5, 2, -3],
                   [4, 5, -4],
                   [6, 4, -4]])

    # Ax = lambda*x
    eigen_data = A.eigenvects()
    # na diagonalu se pricte -lamdba
    # a spocita se determinant
    for eigenval, multiplicity, eigenvecs in eigen_data:
        print(f"Eigenvalue: {eigenval}, Multiplicity: {multiplicity}")
        for vec in eigenvecs:
            print(f"Eigenvector: {vec}")

    # determinant pro kontrolu
    # lambda^3 - 6*lambda^2 - 11*lambda + 6
    lambda_sym = sp.symbols('lambda')
    char_poly = A.charpoly(lambda_sym)
    print("Characteristic Polynomial:", char_poly.as_expr())

def prikladek2():
    # singular 3x3 matrix with just 1s
    A = sp.Matrix([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]])
    eigen_data = A.eigenvects()
    for eigenval, multiplicity, eigenvecs in eigen_data:
        print(f"Eigenvalue: {eigenval}, Multiplicity: {multiplicity}")
        for vec in eigenvecs:
            print(f"Eigenvector: {vec}")
    # (A-lambda*E)x     = theta
    # det(A - lambda*E) = 0 = -lambda^3 + 3*lambda^2 = lambda^2(-lambda + 3)
    # lambda1 = 0, lambda2 = 3

def prikladek3():
    # diagonal matrix
    # (3 1 -1)
    # (0 2 0)
    # (1 1 1)

    A = sp.Matrix([[3, 1, -1],
                     [0, 2, 0],
                     [1, 1, 1]])

    eigen_data = A.eigenvects()
    for eigenval, multiplicity, eigenvecs in eigen_data:
        print(f"Eigenvalue: {eigenval}, Multiplicity: {multiplicity}")
        for vec in eigenvecs:
            print(f"Eigenvector: {vec}")


if __name__ == "__main__":
    #main()
    prikladek3()
#
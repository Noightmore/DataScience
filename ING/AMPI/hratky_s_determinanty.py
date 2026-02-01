import numpy as np
import sympy as sp

# matlab commands used: inv(), det(), syms

# kdy je matice regularni a jaka je jeji inverze?

def prklad1():
    # ( 2 3 )
    # ( 5 3 )

    A = sp.Matrix([[2, 3],
                   [5, 3]])

    det_A = A.det()

    # adjunct of a matrix:
    A_adj = A.adjugate()
    print("Adjugate of A:\n", A_adj)

    # inverse via adj/det:

    A_inv = A_adj/det_A
    print("Inverse of A via adj matrix:\n", A_inv)

    print("Determinant of A:", det_A)
    if det_A != 0:
        A_inv = A.inv()
        print("Inverse of A:\n", A_inv)
    else:
        print("Matrix A is singular and does not have an inverse.")


def prklad2():
    # ( cos(a) -sin(a) )
    # ( sin(a)  cos(a) )

    a = sp.symbols('a')
    A = sp.Matrix([[sp.cos(a), -sp.sin(a)],
                   [sp.sin(a), sp.cos(a)]])

    # podminka regularity: det(A) != 0
    det_A = A.det()
    assert det_A != 0, "Matrix is singular!"
    print("Determinant of A:", det_A)


def prklad3():
    # ( 3i 1 2-i )
    # ( 0  3  5  )
    # ( 2i i 3+i )

    i = sp.I
    A = sp.Matrix([[3*i, 1, 2 - i],
                   [0, 3, 5],
                   [2*i, i, 3 + i]])

    det_A = A.det()
    print("Determinant of A:", det_A)

    assert det_A != 0, "Matrix is singular!"

    adj_A = A.adjugate()
    print("Adjugate of A:\n", adj_A)

    inv_A = adj_A/det_A
    print("Inverse of A via adj matrix:\n", inv_A)

    # why is determinant 25 and full number without imaginary part?
    # explanation: the imaginary parts cancel out in the determinant calculation,
    # we just sum the signs of each permutation

    # vzorec pro rozvoj determinantu:
    # detA = sum(-1^(i+k) alpha_ik det(A(i,k)) i=1 to n
    # asi?????
    # :(
if __name__ == "__main__":
    prklad3()

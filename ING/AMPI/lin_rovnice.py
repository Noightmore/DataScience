# in python use sympy for symbolic mathematics
import numpy as np
import sympy as sp

def priklad1():
    # x - y + z - t = 0
    # matlab prikazy: null, rank, datovy typ sym,  A\b

    # frobeniova veta:
    # a) soustava ma reseni prave kdyz rank(A) = rank([A|b])
    # b) S = x_tilde + S0 ; dim(S0) = n - rank(A)

    # define symbols
    x, y, z, t = sp.symbols('x y z t')
    # define the equation
    equation = sp.Eq(x - y + z - t, 0)
    # solve the equation
    solution = sp.solve(equation, x)
    print("Solution for x in terms of y, z, t:", solution)
    A = sp.Matrix([[1, -1, 1, -1]])
    rank_A = A.rank() #; bod a)
    print("Rank of matrix A:", rank_A)
    null_space = A.nullspace()
    print("Null space of matrix A:", null_space) # b; null(A) = S0 =

    # in matlab:
    # A = [1 -1 1 -1];
    # b = 0;
    # rank(A)  # in python: rank_A = sp.Matrix([[1, -1, 1, -1]]).rank() ; bod a)
    # jadro zobrazeni: null(A)  # in python: null_space = A.nullspace()

def priklad241():
    # dalsi priklad 241:
    # 4x - 2y + 5z - t = 0
    # -2x + 5y - 2z + 4t = 0
    # 2x + 4y + 3z - t = 0
    # 5x + 4y + 7z + t = 0

    A2 = sp.Matrix([[4, -2, 5, -1],
                    [-2, 5, -2, 4],
                    [2, 4, 3, -1],
                    [5, 4, 7, 1]])
    rank_A2 = A2.rank()
    print("Rank of matrix A2:", rank_A2) # hodnost matice = rank(A)
    null_space_A2 = A2.nullspace()
    print("Null space of matrix A2:", null_space_A2) # S0 = null(A2)

    # Rank of matrix A2: 4
    # Null space of matrix A2: []
    # S = S0 = {0}  => jedine reseni je trivialni reseni; jen nulovy vektor
    # dim(S0) = n - rank(A) = 4 - 4 = 0

def priklad240():
    # 3x + y  + 0z - 2t = 0
    # -2x - 4y + 5z - 9t = 0
    # 3x + y + 0z  + t =  0

    A3 = sp.Matrix([[3, 1, 0, -2],
                    [-2, -4, 5, -9],
                    [3, 1, 0, 1]])

    rank_A3 = A3.rank()
    print("Rank of matrix A3:", rank_A3) # hodnost matice = rank(A)
    null_space_A3 = A3.nullspace()
    print("Null space of matrix A3:", null_space_A3) # S0 = null(A3)

    #Rank of matrix A3: 3
    #Null space of matrix A3: [Matrix([
    #    [-1/2],
    #    [ 3/2],
    #    [   1],
    #    [   0]])]
    # z toho linearni obal, lambda na indexu)

    # dim(S0) = n - rank(A) = 4 - 3 = 1

# nehomogenni soustava
def priklad248():
    # x + y + z + u + v = 1

    A4 = sp.Matrix([[1, 1, 1, 1, 1]])
    b4 = sp.Matrix([[1]])
    rank_A4 = A4.rank()
    Ab4 = A4.row_join(b4)
    rank_Ab4 = Ab4.rank()
    print("Rank of matrix A4:", rank_A4) # hodnost matice = rank(A)
    print("Rank of augmented matrix [A4|b4]:", rank_Ab4) # hodnost matice = rank([A|b])
    null_space_A4 = A4.nullspace()
    print("Null space of matrix A4:", null_space_A4) # S0 = null(A4)
    null_space_Ab4 = Ab4.nullspace()
    print("Null space of augmented matrix [A4|b4]:", null_space_Ab4) # S0 = null([A4|b4])

    # reseni jen kdyz:
    # h(odnost(A) = hodnost([A|b]) => reseni existuje
    print(rank_Ab4 == rank_A4) # True

    # S = x_tilde + S0 ; dim(S0) = n - rank(A)
    print("Dimension of null space S0:", 5 - rank_A4) # dim(S0) = n - rank(A)

    # A\b in matlab:
    # in python:
    # x_tilde = A4.LUsolve(b4) nefunguje :(
    x_tilde = A4.pinv() * b4

    print("Particular solution x_tilde:", x_tilde) # da jedno konkretni reseni, muze se lisit od matlabu
    # S = x_tilde + S0

def priklad248_2():
    # x + 2y + 3z - t = 1
    # 3x + 2y + z - t = 1
    # 2x + 3y + z + t = 1
    # 2x + 2y + 2z - t = 1
    # 5x + 5y + 2z + 0t = 3

    A5 = sp.Matrix([[1, 2, 3, -1],
                    [3, 2, 1, -1],
                    [2, 3, 1, 1],
                    [2, 2, 2, -1],
                    [5, 5, 2, 0]])

    b5 = sp.Matrix([[1],
                   [1],
                   [1],
                   [1],
                   [3]]) # kdyz misto 3 je 2 tak to reseni ma
    rank_A5 = A5.rank()
    Ab5 = A5.row_join(b5)
    rank_Ab5 = Ab5.rank()

    x_tilde = A5.pinv() * b5

    # h(odnost(A) = hodnost([A|b]) => reseni existuje
    # S = x_tilde + S0 ; dim(S0) = n - rank(A)

    print("Particular solution x_tilde:", x_tilde)
    print("Dimension of null space S0:", 4 - rank_A5) # dim(S0) = n - rank(A)
    print(rank_Ab5 == rank_A5) # False

def priklad266():
    # lambda*x + y + z = 1
    # x + lambda*y + z = 1
    # x + y + lambda*z = 1

    # reste pro lambda z R
    lambda_sym = sp.symbols('lambda')
    A6 = sp.Matrix([[lambda_sym, 1, 1],
                    [1, lambda_sym, 1],
                    [1, 1, lambda_sym]])

    b6 = sp.Matrix([[1],
                     [1],
                     [1]])
    rank_A6 = A6.rank()
    Ab6 = A6.row_join(b6)
    rank_Ab6 = Ab6.rank()
    print("Rank of matrix A6:", rank_A6)
    print("Rank of augmented matrix [A6|b6]:", rank_Ab6)
    print("Dimension of null space S0:", 3 - rank_A6) # dim(S0) = n - rank(A)
    print(rank_Ab6 == rank_A6)

    x_tilde = A6.pinv() * b6
    x_tilde = np.real(x_tilde)
    print("Particular solution x_tilde:", x_tilde)

    # lambda by melo byt rozne od -2 a 1; zjistili jsme to pres determinant
    # tenhle priklad je hodne bruh; vraci sileny reseni, nutno ho upravit temito podminkami

    # pak se jeste da dosadit konkretni hodnota lambda pro zjisteni kdy je matice regularni a kdy singularni

    # na dotaz rank(A) vraci 3 a ignoruje symbolickou promennou lambda; to dela jak python, tak matlab

def exam_1():
    """
    234. Nechť hodnost matice homogenní soustavy lineárních rovnic je o jednotku menší než počet neznámých.
    Pak libovolná dvě řešení této soustavy mají tu vlastnost, že jedno z nich je násobkem druhého. Dokažte.
    """

    # prove:
    # nechť máme soustavu Ax = 0, kde A je matice koeficientů a x je vektor neznámých
    # nechť rank(A) = n - 1, kde n je počet neznámých
    # pak dim(Null(A)) = n - rank(A) = n - (n - 1) = 1
    # tedy jádro zobrazení má dimenzi 1, což znamená, že všechna řešení jsou lineárně závislá
    # vsechny vektory reseni lze zapsat jako nasobky jednoho nenuloveho vektoru


def exam_2():
    """
    236. Budiž dána nehomogenní soustava lineárních rovnic (řešitelná) a lineární kombinace jejích řešení.
    Kdy je tato kombinace řešením této soustavy?
    """

    # prove:
    # nechť máme nehomogenní soustavu Ax = b, kde A je matice koeficientů, x je vektor neznámých a b je vektor pravých stran
    # nechť x1 a x2 jsou dvě řešení této soustavy, tedy Ax1 = b a Ax2 = b
    # nechť c1 a c2 jsou libovolné skaláry
    # pak lineární kombinace x = c1*x1 + c2*x2 je řešením soustavy, pokud c1 + c2 = 1

def exam_3():
    """
    237. Nalezněte nutnou a postačující podmínku pro to, aby řešením dané soustavy lineárních rovnic (řešitelné) byl:
    a) součet jejích libovolných dvou řešení;
    b) násobek libovolného jejího řešení pevně zvoleným číslem α ∈ T, α ≠ 1.
    """

    # prove:
    # a)
    # nechť máme nehomogenní soustavu Ax = b, kde A je matice koeficientů, x je vektor neznámých a b je vektor pravých stran
    # nechť x1 a x2 jsou dvě řešení této soustavy, tedy Ax1 = b a Ax2 = b
    # pak součet x = x1 + x2 je řešením soustavy, pokud b = 0 (tedy soustava je homogenní)
    # b)
    # nechť máme nehomogenní soustavu Ax = b, kde A je matice koeficientů, x je vektor neznámých a b je vektor pravých stran
    # nechť x1 je řešení této soustavy, tedy Ax1 = b



if __name__ == "__main__":
    #priklad241()
    #priklad240()
    #priklad248_2()
    priklad266()

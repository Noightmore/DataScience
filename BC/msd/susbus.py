from sympy import symbols, exp, diff, log, Sum, latex
from IPython.display import display


B, G, a, ny, x = symbols('B G a ny x')

N = 100
function_of_x = B / ((2 * a * G) / B) + exp(-abs(x - ny) / a)**B

# Print the function
#print("Original Function:")
#print(function_of_x)

# LME: d_function_of_x/d_ny sum_over_x(log(function_of_x))

LME = Sum(log(function_of_x), (x, 1, N))

#print("LME:")
#print(LME)

# d_function_of_x/d_ny
d_function_of_x_d_ny = diff(LME, ny)

l = latex(d_function_of_x_d_ny)
display(l)
#print(l)

# second derivative
d2_function_of_x_d_ny2 = diff(d_function_of_x_d_ny, ny)

l = latex(d2_function_of_x_d_ny2)
display(l)

print(d2_function_of_x_d_ny2)


# very bruh sus


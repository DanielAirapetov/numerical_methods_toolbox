import numpy as np
import sympy as sp



def goldenSectionMethod(a, b, delta, flag, sym_func):

    x = sp.Symbol('x')
    f = sp.lambdify(x, sym_func, "numpy")

    phi = (1 + np.sqrt(5)) / 2
    error = float('inf')
    iterations = 0
    max_iter = 1000

    x1 = b - ((b - a) / phi)
    x2 = a + ((b - a) / phi)

    while error > delta and iterations < max_iter:

        if flag == 1:
            if f(x1) >= f(x2):
                a = x1
                x1 = x2
                x2 = a + ((b - a) / phi)
            else:
                b = x2
                x2 = x1
                x1 = b - ((b - a) / phi)

        elif flag == 2:
            if f(x1) <= f(x2):
                a = x1
                x1 = x2
                x2 = a + ((b - a) / phi)
            else:
                b = x2
                x2 = x1
                x1 = b - ((b - a) / phi)

        error = np.abs(b - a)
        iterations += 1

    return ((a + b) / 2), iterations


def newtonMinMaxMethod(x0, delta, sym_func):

    x = sp.Symbol('x')

    iterations = 0
    max_iter = 1000
    error = float('inf')

    sym_f_first = sp.diff(sym_func, x)
    sym_f_second = sp.diff(sym_func_first, x)

    f = sp.lambdify(x, sym_func, "numpy")
    f_first = sp.lambdify(x, sym_f_first, "numpy")
    f_second = sp.lambdify(x, sym_f_second, "numpy")


    alpha = 1

    while error > delta and iterations < max_iter:

        x_next = x0 - (alpha * (f_first.subs(x, x0) / f_second.subs(x, x0)))
        error = np.abs(x_next - x0)
        x0 = x_next
        iterations += 1

    return x_next, iterations


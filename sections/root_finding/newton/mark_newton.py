import numpy as np
import sympy as sp

x = sp.symbols('x')

def newtonMethod(x0, delta, flag, f):

    f_prime = sp.diff(f, x)
    x1 = 0

    error = float('inf')

    iter = 0
    max_iter = 1000

    while error >= delta and iter < max_iter:

        if f.subs(x, x0) == 0:
            x1 = x0
            break

        iter += 1

        while f_prime.subs(x, x0) == 0:
            print("x0 is near a local max/min | re-select x0: ")
            x0 = int(input())

        x1 = x0 - (f.subs(x, x0) / f_prime.subs(x, x0))

        if flag == 1:
            error = np.abs(x0 - x1)
        elif flag == 2:
            error = np.abs(x1 - x0) / np.abs(x1)
        elif flag == 3:
            error = np.abs(f.subs(x, x1))
        elif flag == 4:
            if np.abs(x0 - x1) < delta and np.abs(f.subs(x, x1)) < delta:
                return x1, iter
        else:
            print("Invalid flag:")
            flag = int(input("Re-select flag (1-4): "))

        if error > delta:
            x0 = x1

    return x1, iter


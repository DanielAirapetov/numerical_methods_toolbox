import numpy as np


def falsePositionMethod(x0, x1, delta, flag, f):

    x = 0
    x2 = 0
    error = float('inf')

    iter = 0
    max_iter = 1000

    while f(x0) * f(x1) >= 0:
        print("Invalid x0, x1")
        print("Re-enter:")
        x0 = float(input("x0: "))
        x1 = float(input("x1: "))


    x = x1

    while error >= delta and iter < max_iter:
        
        iter += 1

        x2 = x1 - (f(x1) * ((x0 - x1) / (f(x0) - f(x1))))

        if f(x2) == 0:
            break

        if f(x0) * f(x2) < 0:
            x1 = x2
        else:
            x0 = x2

        if flag == 1:
            error = np.abs(x - x2)
        elif flag == 2:
            error = np.abs(x - x2) / np.abs(x2)
        elif flag == 3:
            error = np.abs(f(x2))
        elif flag == 4:
            if np.abs(x - x2) < delta and np.abs(f(x2)) < delta:
                return x2, iter
        else:
            print("Invalid flag")
            flag = int(input("Re-select flag (1-4):"))

        x = x2

    return x2, iter

import numpy as np

def bisectionMethod(x1, x2, delta, flag, f):

    x3 = 0
    x4 = 0

    error = 100000 
    iter = 0
    max_iter = 1000

    while error >= delta and iter <= max_iter:

        iter += 1

        if f(x1) * f(x2) > 0:
            print("Function does not change sign between ", x1, " and ", x2)
            print("Reselect:")
            x1 = input("x1: ")
            x2 = input("x2: ")
        else:
            x3 = (x1 + x2) / 2

            if f(x3) == 0:
                return x3, iter
            if f(x1) * f(x3) < 0:
                x2 = x3
                x4 = x1
            else:
                x1 = x3
                x4 = x2


            if flag == 1:
                error = np.abs(x3 - x4)
            elif flag == 2:
                error = np.abs(x3 - x4) / np.abs(x3)
            elif flag == 3:
                error = np.abs(f(x3))
            elif flag == 4:
                if np.abs(f(x3)) < delta and np.abs(x3 - x4) < delta:
                    return x3, iter
            else:
                print("Flag input is invalid")
                flag = input("Reselect the flag (1-4):")

    return x3, iter

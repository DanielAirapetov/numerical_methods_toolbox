import numpy as np


def secantMethod(x0, x1, delta, flag, f):

    x2 = 0

    error = float('inf')

    iter = 0
    max_iter = 1000

    
    if np.abs(f(x0)) < np.abs(f(x1)):
        x0 = x0 ^ x1
        x1 = x0 ^ x1
        x0 = x0 ^ x1


    while error >= delta and iter < 1000:

        iter += 1

        x2 = x1 - (f(x1) * ((x0 - x1) / (f(x0) - f(x1))))
        x0 = x1
        x1 = x2

        if f(x2) == 0:
            break

        if flag == 1:
            error = np.abs(x0 - x1)
        elif flag == 2:
            error = np.abs(x0 - x1) / np.abs(x1)
        elif flag == 3:
            error = np.abs(f(x1))
        elif flag == 4:
            if np.abs(x0 - x1) < delta and np.abs(f(x1)) < delta:
                return x2, iter
        else:
            print("Invalid flag")
            flag = int(input("Re-select flag (1-4):"))
       

    return x2, iter

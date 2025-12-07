import numpy as np
import math


def hadamardWalsh2(f):

    N = len(f)
    n = int(math.log(N, 2))
    x = f.copy()
    y = np.zeros(N)


    for j in range(1, n + 1):

        s = 0

        for r in range(pow(2, j - 1)):

            for k in range(s, int(N / 2)):

                y[k] = x[k] + x[k + int(N/2)]

            for k in range(int(N/2), N):

                y[k] = x[k - int(N/2)] - x[k]

            s += int(N/2)

        x = y.copy()


    return y

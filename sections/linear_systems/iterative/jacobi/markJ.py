import numpy as np
import math


def isDiagonallyDominant(A):
    
    m = A.shape[0]
    sum = 0


    for i in range(m):
 
        pivot = abs(A[i][i])

        for j in range(m):

            if i == j: continue
            sum += abs(A[i][j])

        if pivot < sum:
            return False

        sum = 0

    return True


def completePivoting(A):

    m = A.shape[0]
    i = 0
    j = 0


    while i < m and j < m:

        maxi = i


        for k in range(i, m):
          if abs(A[k][j]) > abs(A[maxi][j]):
            maxi = k
                   

        if A[maxi][j] != 0:
            A[[i, maxi], :] = A[[maxi, i], :]

        i += 1
        j += 1
    
   


def gaussSeidelMethod(A, delta, flag):

    m = A.shape[0]
    iterations = 0
    max_iter = 1000

    error = float('inf')

    prev_x = np.zeros(m)
    x = np.random.rand(m)

    completePivoting(A)

    while error > delta and iterations < max_iter:

        error = 0
        prev_x = x.copy()

        for i in range(m):

            pivot = A[i][i]
            x[i] = A[i][m]

            for j in range(m):

                if i == j: continue
                x[i] -= A[i][j] * prev_x[j]

            x[i] /= pivot

            if flag == 1:
                error += abs(x[i] - prev_x[i])
            elif flag == 2:
                error += pow(x[i] - prev_x[i], 2)

        if flag == 3 or flag == 4:

            for i in range(m):
                sum = 0

                for j in range(m):

                    sum += A[i][j] * x[j]
                
                if flag == 3:
                    error += abs(sum - A[i][m])
                elif flag == 4:
                    error += pow(sum - A[i][m], 2)

            error /= m

            if flag == 2 or flag == 4:
                error = math.sqrt(error)

        iterations += 1


    return x, iterations


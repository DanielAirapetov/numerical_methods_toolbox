import numpy as np

def gaussJordanElimination(A):
    m = A.shape[0]
    i = 0
    j = 0
    maxi = 0
    x = np.zeros(m)

    while i < m and j < m:
        maxi = i
        for k in range(i + 1, m):
            if abs(A[k][j]) > abs(A[maxi][j]):
                   maxi = k

        if A[maxi][j] != 0:
            if maxi != i:
                A[[i, maxi], :] = A[[maxi, i], :]
            for r in range(m):
                if r == i: continue
                coefficient = A[r][j] / A[i][j]
                for c in range(j, m + 1):
                    A[r][c] -= (A[i][c] * coefficient)
        i += 1
        j += 1

    for i in range(m):
        x[i] = A[i][m] / A[i][i]

    return x


m = int(input())
A = np.zeros((m, m + 1))

for i in range(m):
    for j in range(m + 1):
        A[i][j] = float(input())

A_copy = A.copy()

x = gaussJordanElimination(A_copy)
print(x)

for i in range(m):
    b = 0
    for j in range(m):
        b += (A[i][j] * x[j])
    print(b)

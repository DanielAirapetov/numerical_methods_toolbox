import numpy as np

def gaussianEliminationMethod(A):
    m = A.shape[0]
    i = 0
    j = 0
    x = np.zeros(m)
    
    while i < m and j < m:
        maxi = i
        for k in range(i + 1, m):
            if abs(A[k][j]) > abs(A[maxi][j]):
                maxi = k

        if A[maxi][j] != 0:
            if maxi != i:
                A[[i, maxi], :] = A[[maxi, i], :]
            for r in range(i + 1, m):
                coefficient = A[r][j] / A[i][j]
                for c in range(j, m + 1):
                    A[r][c] -= (A[i][c] * coefficient)
        i += 1
        j += 1 
        
    x[m - 1] = A[m - 1][m] / A[m - 1][m - 1]
    row = m - 2
    while row >= 0:
        x[row] = A[row][m]
        for col in range(row + 1, m):
            x[row] -= (A[row][col] * x[col])
        x[row] /= A[row][row]
        row -= 1

    return x

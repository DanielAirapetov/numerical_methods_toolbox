import numpy as np

def gaussian(A):
    n = A.shape[0]
    m = A.shape[1]
    
    i = 0
    j = 0
    
    x = np.zeros(n)
    
    while i < n and j < m - 1:
        maxi = i
        for k in range(i + 1, n):
            if abs(A[k][j]) > abs(A[maxi][j]):
                maxi = k
        if A[maxi][j] != 0:
            if maxi != i:
                A[[i, maxi], :] = A[[maxi, i], :]
            pivot = A[i][j]
            for u in range(i + 1, n):
                A[u][j:] = A[u][j:] - (A[u][j] / pivot) * A[i][j:]
            i += 1
        j += 1
    
        
    x[n - 1] = A[n - 1][m - 1] / A[n - 1] [n - 1]
        
    for i in range(n - 2, -1, -1):
        x[i] = A[i][m - 1]
        for j in range(i + 1, n):
            x[i] = x[i] - A[i][j] * x[j]
        x[i] = x[i] / A[i][i]
            
    return x

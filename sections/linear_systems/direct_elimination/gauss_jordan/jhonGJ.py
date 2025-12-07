import numpy as np

def jordan_gaussian(A):
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
            A[i][j:] = A[i][j:] / A[i][j]
            for u in range(n):
                if u != i:
                    A[u][j:] = A[u][j:] - A[u][j] * A[i][j:]
            
            i += 1
        j += 1
        
    for i in range(n):
        x[i] = A[i][m - 1]
            
    return x

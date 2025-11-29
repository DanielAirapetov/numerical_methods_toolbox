import numpy as np
import math

def gauss_seidel (mat, tolerance, stopping_criterion):
    matrix = mat.copy()
    n = matrix.shape[0]
    x = np.zeros(n)
    old_x = np.zeros(n)
    
    A0 = matrix[:, :n].copy()
    b0 = matrix[:, n].copy()
    
    for i in range(n):
        x[i] = 1
        old_x[i] = x[i]
    
    error = 10
    iterations = 0
    while (error > tolerance):
        iterations += 1
        error = 0
        
        for i in range(n): 
            x[i] = matrix[i, n]
            
            for j in range(n):
                if(i != j):
                    x[i] = x[i] - matrix[i, j] * x[j]
            x[i] = x[i] / matrix[i, i]
            
        if(stopping_criterion == 1):
            error = np.mean(np.abs(x - old_x))
        elif(stopping_criterion == 2):
            error = math.sqrt(np.mean((x - old_x) ** 2))
        elif (stopping_criterion == 3):
            error = np.mean(np.abs(A0 @ x - b0))
        elif (stopping_criterion == 4):
            error = math.sqrt(np.mean((A0 @ x - b0) ** 2))
        
        old_x = x.copy()
    
    return x, iterations

import numpy as np
import math

def jacobi_method (mat, tolerance, stopping_criterion):
    matrix = mat.copy()
    n = matrix.shape[0]
    new_x = np.zeros(n)
    old_x = np.zeros(n)
    
    A0 = matrix[:, :n].copy()
    b0 = matrix[:, n].copy()
    
    for i in range(n):
        new_x[i] = 1
    
    error = 10
    
    while (error > tolerance):
        error = 0
        
        for i in range(n): 
            old_x [i] = new_x[i]
            new_x[i] = matrix[i, n]
        
        for i in range(n):
            for j in range(n):
                if(i != j):
                    new_x[i] = new_x[i] - matrix[i, j] * old_x[j]
            new_x[i] = new_x[i] / matrix[i, i]
            
        if(stopping_criterion == 1):
            error = np.mean(np.abs(new_x - old_x))
        elif(stopping_criterion == 2):
            error = math.sqrt(np.mean((new_x - old_x) ** 2))
        elif (stopping_criterion == 3):
            error = np.mean(np.abs(A0 @ new_x - b0))
        elif (stopping_criterion == 4):
            error = np.sqrt(np.mean((A0 @ new_x - b0) ** 2))
    
    return new_x


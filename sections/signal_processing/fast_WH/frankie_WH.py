import numpy as np
def HadamardWalsh2(f,N):
    x = np.array(f,dtype=float)
    h = 1
    while h < N:
        for j in range(0, N, 2*h): #split loop in half to perform HW transform butterfly
            for k in range(j,j+h): #butterfly operations
                a = x[k]
                b = x[k + h]
                x[k] = a + b        # sum 
                x[k + h] = a - b        # diff
        h*=2 #step by powers of 2 each time
    return x # return final transformed x 


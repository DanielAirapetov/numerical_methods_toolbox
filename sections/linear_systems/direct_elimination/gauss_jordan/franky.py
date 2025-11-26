import numpy as np
def GJ_elim(augmented_matrix):
    A = augmented_matrix.copy()
    n = A.shape[0]
    for i in range(n):
        A[i] /= A[i,i] # multiply row i by 1/aii
        for j in range(n):
            if j != i: #skip pivots
                A[j] -= A[j,i] * A[i] #add -aij time row i to row j

    return A[:,-1] # return last column with solutions

def main():
    matrix1 = np.array([[3,1,-4,7],[-2,3,1,-5],[2,0,5,10]],dtype=float)
    solutions = GJ_elim(matrix1)
    n = matrix1.shape[0]
    for i in range(n):
        print(f"x{i+1} = {solutions[i]}")

if __name__ == "__main__":
    main()
     
    
    
    
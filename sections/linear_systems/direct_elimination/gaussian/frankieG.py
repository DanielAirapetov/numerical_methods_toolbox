import numpy as np
def gauss_elim(A):
    A = A.copy()
    i, j = 0, 0 # initalize indeces (rows i, columns j)
    n = A.shape[0] #get the size of rows and columns
    m = A.shape[1]
    while (i < n and j < m):
        maxi = i
        for k in range(i+1, n):
            if abs(A[k,j]) > abs(A[maxi,j]): #do partial piviting
                maxi = k
        if A[maxi, j] != 0: #check if column has a pivot 
            A[[i, maxi]] = A[[maxi, i]] #swap back to origninal indeces 
            A[i,:] = A[i,:] / A[i,j] # perform the gaussian elim process
            for u in range(i+1, n):
                temp = A[u,j] # store A[u,j] in a temporary variable so it doesnt perform the operation for columns already eliminated
                A[u,:] = A[u,:] - temp * A[i,:] # gaussian elim
            i += 1 #move to next row and column
            j += 1
        else: # column doesnt have pivot so just go to next
            j += 1 
    return A

def back_sub(A):
    n = A.shape[0]
    m = A.shape[1]
    solutions = np.zeros(n)
    
    for i in range(n-1, -1, -1):  # Start from last row, going backwards
        pivot_col = -1
        for j in range(m-1): #search for each columns pivot
            if A[i,j] != 0:
                pivot_col = j # assign pivot column
                break
        
        if pivot_col == -1: # if column has no pivor
            if A[i,-1] != 0: # no solutions row of all 0s except last column
                print("No solution")
                return None
            else:
                solutions[i] = 0  # free variable, all row of all 0s including last column
                continue
        
        solutions[i] = A[i,-1] # now that we found pivot columns, perform back substitution
        for j in range(pivot_col+1, m-1):
            solutions[i] -= A[i,j] * solutions[j]
        solutions[i] /= A[i,pivot_col] # xn = b'n/a'nn
    
    return solutions


def print_solution(list):
    for i in range(len(list)):
        print(f"Solution {i+1} = {list[i]}")
        
def test_roots(roots, A):
    n = A.shape[0]
    m = A.shape[1]
    results = []
    sum = 0.0
    for i in range(n): # iterate over all rows except last one with solutions
        for j in range(m-1): #nxn matrix so i can use same n as rows to iterate over columns
            sum += A[i,j]*roots[j] #multiply root by the constant for each column (except last) and add all together
        if abs(sum - A[i,-1]) < 1e-6: #if the sum of the roots pluged in is the same (or close enough because of rounding) as the last column solution is correct. 
            results.append(1) #append 1 for correct root
        else:
            results.append(-1) #append -1 for incorrect root
        sum = 0 # reset sum for next row
    return results
    

def main():
    matrix1 = np.array([[3,1,-4,7],[-2,3,1,-5],[2,0,5,10]],dtype=float)  #assign matrices from homework, making data type float so gauss elim doesnt have round off errors
    matrix2 = np.array([[1,-2,4,6],[8,-3,2,2],[-1,10,2,4]],dtype=float)
    
    reduced_matrix1 = gauss_elim(matrix1) # perform gaussian elimination
    reduced_matrix2 = gauss_elim(matrix2)
    solutions1 = back_sub(reduced_matrix1) #use backsubstition to get roots of system
    solutions2 = back_sub(reduced_matrix2)
      
    print("Solutions for matrix 1:") #print results
    print_solution(solutions1)

    print("Solutions for matrix 2:")
    print_solution(solutions2)
    
    check1 = []
    check2 = []
    check1 = test_roots(solutions1, matrix1)
    check2 = test_roots(solutions2, matrix2)
    
    for i in range(len(check1)):
        if check1[i] == 1:
            print(f"Solution {i+1} of matrix 1 is correct ")
        elif check1[i] == -1:
            print(f"Soultion {i+1} of matrix 1 is incorrect ")
        else:
            print ("Error: invalid test")
        if check2[i] == 1:
            print(f"Solution {i+1} of matrix 2 is correct ")
        elif check2[i] == -1:
            print(f"Solution {i+1} of matrix 2 is incorrect ")
        else:
            print ("Error: invalid test")
            

if __name__ == '__main__':
    main()
        
            
        
            
            
    
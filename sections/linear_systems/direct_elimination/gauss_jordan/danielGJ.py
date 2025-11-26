def gauss_jordan_elimination(mat):
    # Input validation
    for row in mat:
        for elem in row:
            if not isinstance(elem, (int, float)):
                raise ValueError("All elements of the matrix must be numeric.")
            
    # Partial pivoting
    for i in range(len(mat)):
        if mat[i][i] == 0:
            for j in range(i + 1, len(mat)): 
                if mat[j][i] != 0:
                    mat[i], mat[j] = mat[j], mat[i]
                    break
            else:
                raise ZeroDivisionError("Zero pivot encountered, cannot swap rows to continue Gauss-Jordan elimination.")

    # Creating identity matrix
    for i in range(len(mat)): # Work on one column at a time
        pivot = mat[i][i]
        if pivot == 0:
            raise ZeroDivisionError("Zero pivot encountered during normalization, system may be singular.")
        for j in range(len(mat[0])): # Make the pivot equal to 1
            mat[i][j] /= pivot

        # Make all other elements in the column equal to 0
        for j in range(len(mat)): # Iterate over each row
            if j != i: # Skip over the pivot row
                factor = mat[j][i] # Store this value 
                for k in range(len(mat[0])): # Iterate over each element
                    mat[j][k] -= factor * mat[i][k]
    
    # Get the list of solutions
    solutions = []
    for i in range(len(mat)):
        solutions.append(mat[i][len(mat[0]) - 1])
    return solutions
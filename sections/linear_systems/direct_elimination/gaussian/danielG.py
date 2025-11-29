def gaussian_elimination(mat):
    # Input validation
    for row in mat:
        for elem in row:
            if not isinstance(elem, (int, float)):
                raise ValueError("All elements of the matrix must be numeric.")
    
    # Initial partial pivoting
    for i in range(len(mat)):
        if mat[i][i] == 0:  # if pivot == 0, then search for a row to swap it with
            for j in range(i + 1, len(mat)):
                if mat[j][i] != 0:
                    mat[i], mat[j] = mat[j], mat[i]
                    break
            else: 
                raise ZeroDivisionError("Zero pivot encountered, cannot swap rows to continue.")

    # Creating triangular matrix
    for col in range(len(mat[0]) - 1):  # Eliminate an unknown for each iteration
        for i in range(col + 1, len(mat)):  # Go to the next equation for each iteration
            
            if mat[col][col] == 0:  # if pivot becomes zero after elimination, pivot again
                for k in range(col + 1, len(mat)):
                    if mat[k][col] != 0:
                        mat[col], mat[k] = mat[k], mat[col]
                        break
                else:
                    raise ZeroDivisionError("Zero pivot encountered, cannot proceed with elimination.")
            # >>> END FIX <<<

            factor = mat[i][col] / mat[col][col]  # Store this value
            for j in range(col, len(mat[i])):  # Apply the formula to each element
                mat[i][j] -= factor * mat[col][j]
    
    # Back substitution
    solutions = []
    for i in range(len(mat) - 1, -1, -1):  # Start at the last unknown, iterate backwards until the first unknown is reached
        b = mat[i][len(mat[0]) - 1]
        term = 0
        for j in range(i + 1, len(mat)):
            term += mat[i][j] * solutions[len(mat) - 1 - j]
        a = mat[i][i]
        if a == 0:
            raise ZeroDivisionError("Zero pivot encountered during back-substitution, system may be singular.")
        solutions.append((b - term) / a)
    solutions.reverse()
    return solutions

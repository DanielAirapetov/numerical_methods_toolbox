def gauss_seidel_iterative_method(mat, tol, flag):
    # Input validation
    for row in mat:
        for elem in row:
            if not isinstance(elem, (int, float)):
                raise ValueError("All elements of the matrix must be numeric.")
            
    # Verify the matrix is diagonally dominant, if not make it so
    diagonally_dominant = True
    for i in range(len(mat)):
        summation = 0
        for j in range(len(mat)):
            summation += abs(mat[i][j])
        if abs(mat[i][i]) < summation - abs(mat[i][i]):
            diagonally_dominant = False
            break
    if not diagonally_dominant:
        n = len(mat)
        row_sums = [sum(abs(mat[row][j]) for j in range(n)) for row in range(n)]
        used = [False]*n
        assignment = []
        for i in range(n):
            best_row = -1
            best_score = float('-inf')
            for row in range(n):
                if not used[row]:
                    pivot = abs(mat[row][i])
                    summation = row_sums[row] - pivot
                    score = pivot - summation
                    if score > best_score:
                        best_score = score
                        best_row = row
            assignment.append(best_row)
            used[best_row] = True
        mat[:] = [mat[assignment[i]] for i in range(n)]

    if flag not in [1, 2, 3, 4]:
        raise ValueError("Invalid flag. Expected one of [1, 2, 3, 4].")    
    
    a = [row[:] for row in mat]
    n = len(a)
    biases = [row[-1] for row in a]
    new_x = [1 for row in a]
    old_x = new_x.copy()

    for i in range(n):
        if a[i][i] == 0:
            raise ZeroDivisionError("Zero diagonal element encountered — cannot perform iteration.")
        biases[i] = biases[i] / a[i][i]
        for j in range(n):
            if i != j:
                a[i][j] = a[i][j] / a[i][i]

    iter = 0
    error = tol + 1
    while error > tol:
        error = 0
        old_x = new_x.copy()
        for i in range(n):
            new_x[i] = biases[i]
        
        match flag:
            case 1:
                for j in range(n):
                    for k in range(n):
                        if j != k:
                            new_x[j] -= a[j][k] * new_x[k]
                    error += abs(new_x[j] - old_x[j])
                error /= n

            case 2:
                for j in range(n):
                    for k in range(n):
                        if j != k:
                            new_x[j] -= a[j][k] * new_x[k]
                    error += (new_x[j] - old_x[j]) ** 2
                error = (error / n) ** 0.5 

            case 3:
                for j in range(n):
                    for k in range(n):
                        if j != k:
                            new_x[j] -= a[j][k] * new_x[k]
                for i in range(n):
                    summation = 0
                    for j in range(n):
                        summation += a[i][j] * new_x[j]
                    error += abs(summation - biases[i])
                error /= n

            case 4:
                for j in range(n):
                    for k in range(n):
                        if j != k:
                            new_x[j] -= a[j][k] * new_x[k]
                for i in range(n):
                    summation = 0
                    for j in range(n):
                        summation += a[i][j] * new_x[j]
                    error += (summation - biases[i]) ** 2
                error = (error / n) ** 0.5

        iter += 1
        if (iter > 1000): # check if iterations has exceeded a "ridiculous" value (1000)
            print("\nIterations have exceeded 1000, terminating the Gauss-Seidel function.") 
            break
        
    return new_x, iter
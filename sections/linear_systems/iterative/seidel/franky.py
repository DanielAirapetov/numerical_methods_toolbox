def GaussSiedel(arr, start_values, tolerance, flag):
    A0 = arr[:,:-1].copy()
    b0 = arr[:,-1].copy()
    arr = arr.copy()
    i, j = 0, 0 # initalize indeces (rows i, columns j)
    A = arr[:,:-1]
    n = A.shape[0] #get the size of rows and columns
    m = A.shape[1] 
    while (i < n and j < m):
        maxi = i
        for k in range(i+1, n):
            if abs(A[k,j]) > abs(A[maxi,j]): #do partial piviting
                maxi = k
        if A[maxi, j] != 0: #check if column has a pivot 
            arr[[i, maxi]] = arr[[maxi, i]] #swap back to origninal indeces 
            A = arr[:, :-1]   # refresh view after swap
            i += 1 #move to next row and column
            j += 1
        else: # column doesnt have pivot so just go to next
            j += 1
    A = arr[:,:-1].copy()
    b = arr[:,-1].copy()  # fixed: take b from arr, not A
    new_x = np.zeros(len(start_values))
    old_x = np.zeros(len(new_x))
    
    for i in range(n):
        b[i] = b[i]/A[i,i]
        new_x[i] = start_values[i]
        old_x[i] = new_x[i]
        for j in range(n):
            if(i!=j):
                A[i,j] /= A[i,i]

    error = 10           
    iter = 0              
    max_iter = 1000       

    while (error > tolerance) and (iter < max_iter):   
        old_x[:] = new_x  # reset old_x 

        max_error = 0      
        for i in range(n):
            new_x[i] = b[i]
            for j in range(n):
                if(i!=j):
                    new_x[i] -= A[i,j]*new_x[j]
            if flag == 1:  # approximate mean abs err
                curr_err = np.mean(np.abs(new_x[i] - old_x[i]))
            elif flag == 2:  # root mean squared err
                curr_err = np.sqrt(np.mean((new_x[i] - old_x[i])**2))
            elif flag == 3:  # true mean abs err
                curr_err = np.mean(np.abs(A0 @ new_x - b0))
            elif flag == 4:  # true rmse
                curr_err = np.sqrt(np.mean((A0 @ new_x - b0)**2))
            else:
                curr_err = 0  # avoid undefined vars for invalid flag

            max_error = max(max_error, curr_err)

        error = max_error 
        iter += 1

        if iter >= max_iter and error > tolerance:
            print("Warning: Gauss-Siedel did not converge (hit max_iter).")

    return new_x, iter  
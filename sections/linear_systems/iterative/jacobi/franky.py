import numpy as np

def jacobi_method(augmented_matrix, tolerance, flag, max_iter=1000):
    A = augmented_matrix[:, :-1]
    b = augmented_matrix[:, -1]
    n = A.shape[0]
    
    x_old = np.ones(n)  # default initial guess [1, 1, ..., 1]
    x_new = np.ones(n)

    # Keep original A and b for residual-based errors
    A_orig = A.copy()
    b_orig = b.copy()

    iter_count = 0

    while iter_count < max_iter:
        for i in range(n):
            sum_ = np.dot(A[i, :], x_old) - A[i, i] * x_old[i]
            x_new[i] = (b[i] - sum_) / A[i, i]

        # -------- Stopping Criteria --------
        if flag == 1:  # Approximate MAE
            error = np.mean(np.abs(x_new - x_old))
        elif flag == 2:  # Approximate RMSE
            error = np.sqrt(np.mean((x_new - x_old)**2))
        elif flag == 3:  # True MAE (residual)
            residual = np.dot(A_orig, x_new) - b_orig
            error = np.mean(np.abs(residual))
        elif flag == 4:  # True RMSE (residual)
            residual = np.dot(A_orig, x_new) - b_orig
            error = np.sqrt(np.mean(residual**2))
        else:
            raise ValueError("Invalid stopping flag (must be 1 to 4)")

        if error <= tolerance:
            return x_new, iter_count + 1

        x_old = x_new.copy()
        iter_count += 1
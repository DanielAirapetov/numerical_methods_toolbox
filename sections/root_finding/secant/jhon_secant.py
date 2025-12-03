def secant_method(x0, x1, tolerance, flag, user_function):
    estimated_root = None
    x2 = None
    estimated_root_found = False
    i = 0
    
    if abs(user_function(x0)) < abs(user_function(x1)):
        x0, x1 = x1, x0
        
    while not(estimated_root_found) and i <= 1000:
        i += 1
        x2 = x1 - user_function(x1) * (x0 - x1) / (user_function(x0) - user_function(x1))
        
        x0 = x1
        x1 = x2
        
        if user_function(x2) == 0:
            estimated_root = x2
            estimated_root_found = True
        else:
            if flag == 1:
                if abs(x0 - x1) < tolerance:
                    estimated_root = x1
                    estimated_root_found = True
            elif flag == 2:
                if (abs(x0 - x1) / abs(x1)) < tolerance:
                    estimated_root = x1
                    estimated_root_found = True
            elif flag == 3:
                if user_function(x1) < tolerance:
                    estimated_root = x1
                    estimated_root_found = True
            else:
                if (abs(x0 - x1) < tolerance) and (user_function(x1) < tolerance):
                    estimated_root = x1
                    estimated_root_found = True
    
    return estimated_root, i


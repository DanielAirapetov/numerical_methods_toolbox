def newton_method(x0, tolerance, flag, user_function):
    i = 0
    x1 = None
    estimated_root = None
    estimated_root_found = False
    
    while not(estimated_root_found) and i <= 1000:
        if user_function(x0) == 0:
            estimated_root = x0
            estimated_root_found = True
        else:
            if user_function(x0, 1) == 0:
                x0 = float(input("Please enter a x0: "))
            else:
                x1 = x0 - (user_function(x0) / user_function(x0, 1))
                
                if flag == 1:
                    if abs(x1 - x0) < tolerance:
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
                elif flag == 2:
                    if (abs(x1 - x0) / abs(x1)) < tolerance:
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
                elif flag == 3:
                    if (abs(user_function(x1)) < tolerance):
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
                else:
                    if (abs(x1 - x0) < tolerance) and (abs(user_function(x1)) < tolerance):
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
    
    return estimated_root, i

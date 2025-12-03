def false_position_method(x0, x1, tolerance, flag, user_function):
    while (user_function(x0) * user_function(x1)) < 0:
        x0 = float(input("Incorrect x0. Please enter another one: "))
        x1 = float(input("Incorrect x1. Please enter another one: "))
    
    x = None
    x2 = None
    estimated_root = None
    estimated_root_found = False
    i = 0
    
    x = x1
        
    while not(estimated_root_found) and i <= 1000:
        i += 1
        
        x2 = x1 - user_function(x1) * ((x0 - x1) / (user_function(x0) - user_function(x1)))
        
        if user_function(x2) == 0:
            estimated_root = x2
            estimated_root_found = True
        else:
            if (user_function(x0) * user_function(x2)) < 0:
                x1 = x2
            else:
                x0 = x2
                
            if flag == 1:
                if abs(x - x2) < tolerance:
                    estimatedRoot = x2
                    estimatedRootFound = True
                else:
                    x = x2
            elif flag == 2:
                if (abs(x - x2) / abs(x2)) < tolerance:
                    estimated_root = x2
                    estimated_root_found = True
                else:
                    x = x2
            elif flag == 3:
                if user_function(x2) < tolerance:
                    estimated_root = x2
                    estimated_root_found = True
                else:
                    x = x2
            else:
                if (abs(x - x2) < tolerance) and (user_function(x2) < tolerance):
                    estimated_root = x2
                    estimated_root_found = True
                else:
                    x = x2
    
    return estimated_root, i


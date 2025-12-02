def bisection(x1, x2, tolerance, flag, user_function):
    while (user_function(x1) * user_function(x2)) > 0:
        print("Please pick other brackets: ")
        x1 = float(input("x1: "))
        x2 = float(input("x2: "))
        
    i = 0
    x3 = None
    x4 = None
    estimated_root = None
    estimated_root_found = False
    
    while not(estimated_root_found) and i <= 1000:
        i += 1
        x3 = (x1 + x2) / 2
        
        if user_function(x3) == 0:
            estimated_root = x3
            estimated_root_found = True
        else:
            if (user_function(x1) * user_function(x3)) < 0:
                x2 = x3
                x4 = x1
            else:
                x1 = x3
                x4 = x3
            
            if flag == 1:
                if abs(x3 - x4) < tolerance:
                    estimated_root = x3
                    estimated_root_found = True
            elif flag == 2:
                if (abs(x3 - x4) / abs(x3)) < tolerance:
                    estimated_root = x3
                    estimated_root_found = True
            elif flag == 3:
                if abs(user_function(x3)) < tolerance:
                    estimated_root = x3
                    estimated_root_found = True
            else:
                if (abs(x3 - x4) < tolerance) and (abs(user_function(x3) < tolerance)):
                    estimated_root = x3
                    estimated_root_found = True
    
    return estimated_root, i


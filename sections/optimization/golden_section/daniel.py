def golden_section_optimization(a, b, tol, flag, func):
    if flag not in ['min', 'max']:
        raise ValueError("Invalid flag. Expected one of ['min', 'max'].")
    if a > b:
        a, b = b, a
    GOLDEN_SECTION = (1 + 5**0.5) / 2
    x1 = b - (b-a) / GOLDEN_SECTION
    x2 = a + (b-a) / GOLDEN_SECTION
    y1 = func(x1)
    y2 = func(x2)
    iter = 0
    while abs(b-a) > tol:
        if iter > 1000:
            print("Iterations have exceeded 1000, terminating function.")
            break
        match flag:
            case 'min': 
                if y1 >= y2:
                    a = x1
                    x1 = x2
                    x2 = a + (b-a) / GOLDEN_SECTION
                    y1 = y2
                    y2 = func(x2)
                else:
                    b = x2
                    x2 = x1
                    x1 = b - (b-a) / GOLDEN_SECTION
                    y2 = y1
                    y1 = func(x1)
            case 'max':
                if y1 <= y2:
                    a = x1
                    x1 = x2
                    x2 = a + (b-a) / GOLDEN_SECTION
                    y1 = y2
                    y2 = func(x2)
                else:
                    b = x2
                    x2 = x1
                    x1 = b - (b-a) / GOLDEN_SECTION
                    y2 = y1
                    y1 = func(x1)
        iter+=1
    return (a+b)/2, func((a+b)/2), iter
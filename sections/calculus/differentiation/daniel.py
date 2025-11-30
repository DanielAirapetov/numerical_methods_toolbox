import math

def numerical_differentiation(x_value, x_points, y_points, h, flag, degree):
    def lagrangeInterpolation(x_value, x_points, y_points):
        len_points = len(x_points)
        y_value = 0

        for i in range(len_points):
            L = 1
            for j in range(len_points):
                if j != i:
                    L *= (x_value - x_points[j]) / (x_points[i] - x_points[j])
            y_value += L * y_points[i]
        return y_value

    def find_closest_points(x_value, x_points, y_points, flag, degree):
        seen = set()
        unique_x, unique_y = [], []
        for x_i, y_i in zip(x_points, y_points):
            if x_i not in seen:
                seen.add(x_i)
                unique_x.append(x_i)
                unique_y.append(y_i)
        if len(unique_x) < degree + 1:
            raise ValueError(f"Not enough unique points. Need at least {degree + 1}, but only have {len(unique_x)}")
        x_points, y_points = unique_x, unique_y
        
        if (flag != 'c'):
            filtered_x, filtered_y = [], []
            for x_i, y_i in zip(x_points, y_points):
                if x_i >= x_value:
                    filtered_x.append(x_i)
                    filtered_y.append(y_i)
            if len(filtered_x) < degree + 1:
                filtered_x, filtered_y = unique_x, unique_y
            x_points, y_points = filtered_x, filtered_y

        distances = [(x_points[i], y_points[i], abs(x_points[i] - x_value)) for i in range(len(x_points))]
        distances.sort(key = lambda point: point[2])
        distances = distances[:degree + 1]
        sliced_x = [d[0] for d in distances]
        sliced_y = [d[1] for d in distances]
        return sliced_x, sliced_y

    def get_exact_value(x_value, x_points, y_points):
        for i, x in enumerate(x_points):
            if math.isclose(x_value, x, rel_tol = 10**-9, abs_tol = 10**-9):
                return y_points[i]
        return None
    
    # Input validation
    if flag not in ['a', 'b', 'c']:
        raise ValueError("Invalid flag. Expected 'a', 'b', or 'c'.")
    if degree not in [2, 3]:
        raise ValueError("Invalid interpolation degree. Expected 2 or 3.")
    if len(x_points) != len(y_points) or len(x_points) <= degree:
        raise ValueError("The number of x_points and y_points is not valid.")
    if not isinstance(x_value, (int, float)):
        raise ValueError("x_value must be numeric.")
    if not isinstance(h, (int, float)) or h == 0:
        raise ValueError("h must be a non-zero numeric value.")
    for xi in x_points:
        if not isinstance(xi, (int, float)):
            raise ValueError("All x_points must be numeric.")
    for yi in y_points:
        if not isinstance(yi, (int, float)):
            raise ValueError("All y_points must be numeric.")
    if len(set(x_points)) != len(x_points):
        raise ValueError("x_points contains duplicate values, which is invalid for interpolation.")

    match flag:
        case 'a': # 2-points forward difference
            x_points, y_points = find_closest_points(x_value, x_points, y_points, flag, degree)
            f_x0 = get_exact_value(x_value, x_points, y_points)
            if f_x0 is None:
                f_x0 = lagrangeInterpolation(x_value, x_points, y_points)
            f_x1 = get_exact_value(x_value + h, x_points, y_points)
            if f_x1 is None:
                f_x1 = lagrangeInterpolation(x_value + h, x_points, y_points)
            return (f_x1 - f_x0) / h
        
        case 'b': # 3-points forward difference
            x_points, y_points = find_closest_points(x_value, x_points, y_points, flag, degree)
            f_x0 = get_exact_value(x_value, x_points, y_points)
            if f_x0 is None:
                f_x0 = lagrangeInterpolation(x_value, x_points, y_points)
            f_x1 = get_exact_value(x_value + h, x_points, y_points)
            if f_x1 is None:
                f_x1 = lagrangeInterpolation(x_value + h, x_points, y_points)
            f_x2 = get_exact_value(x_value + 2*h, x_points, y_points)
            if f_x2 is None:
                f_x2 = lagrangeInterpolation(x_value + 2*h, x_points, y_points)
            return (-3*f_x0 + 4*f_x1 - f_x2) / (2*h)
        
        case 'c': # 3-points centered difference
            x_points, y_points = find_closest_points(x_value, x_points, y_points, flag, degree)
            f_x0 = get_exact_value(x_value - h, x_points, y_points)
            if f_x0 is None:
                f_x0 = lagrangeInterpolation(x_value - h, x_points, y_points)
            f_x2 = get_exact_value(x_value + h, x_points, y_points)
            if f_x2 is None:
                f_x2 = lagrangeInterpolation(x_value + h, x_points, y_points)
            return (f_x2 - f_x0) / (2*h) # derivative at x1
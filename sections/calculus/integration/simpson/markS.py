import numpy as np


def lagrangeInterpolation(z, x, f, m) :

    # if z is already a point where the function is defined, then we should find its index and return the value of f at that index instead of interpolating
    if z in x:
        index = np.where(z == x)[0]
        return f[index][0]

    # np.argpartition sorts the indices based on how close they are to z and takes the first m nearest indices into the array, points
    points = np.argpartition(np.abs(x - z), m)[:m]
    
    # the variable is used to store the result
    interpolated_value = 0;


    # step through the array of indices
    # the outer loop is the sum of products of the weighting function L at each point and the values of f at each point
    for i in points:

        # the weighting function L_n(z): the lagrangian term of order i
        # this term is initialized as 1 in the outer loop so that it can be computed for each element in the points array
        lagrangian = 1
        
        # inner loop computes the lagrangian term of order i
        for j in points:

            # if the indices i and j are equivalent this will result in a zero division since the difference between x at the same index will be zero and this difference is in the denominator of the lagrangian expression.
            if j == i: continue

            # the lagrangian term is the product of (z - x_j]) / (x_i - x_j) for all elements in the range of points
            lagrangian *= ((z - x[j]) / (x[i] - x[j]))

        # the lagrangian polynomial is the sum of products between the lagrangian term of order i and the value of the function at the point x_i
        interpolated_value += lagrangian * f[i]
    
    return interpolated_value


# Simpson 1/3 Method:   [f(a) + 2*SUM(f(x_2k)) + 4*SUM(f(x_2k-1)) + f(b)] * h/3
def simpsonOneThirdMethod(x, f, h):

    # m is the number of points being used for interpolation, here we use 3 points for a quadratic polynomial
    m = 3

    # n is the number of subintervals, found by the length of the entire interval divided by the step
    n = int((x[-1] - x[0]) / h)

    # n needs to be an even number for this method to work correctly
    if n & 1 == 1:
        print("Simpson's Method requires an even number of intervals, n is not even.")
        return 0


    # first add the first and last element, the bounds of the integral
    integral = f[0] + f[-1]

    # summation of values of the functions at each subinterval, not including the bounds
    for i in range (1, n):
        
        # I round z to the nearest 8 decimal places to avoid a floating-point error that was occuring when calculating z
        z = round(x[0] + (i * h), 8)

        # for both cases, the value of the function at point z will be evaluated if it isn't known from the table | if it is known then it will be returned from table
        if i & 1 == 0:
            # even bounds of subintervals are seen twice by this method
            integral += (2 * lagrangeInterpolation(z, x, f, m))
        else:
            # odd bounds are seen 4 times
            integral += (4 * lagrangeInterpolation(z, x, f, m))

    # multiply by h and divide by 3
    return integral * (h / 3)


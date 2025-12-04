import numpy as np 

def bit_reverse(arr):
    arr = np.asarray(arr)
    N = arr.shape[0] 
    reversed_arr = np.empty_like(arr)
    for i in range(N):
        x = i
        y = 0
        for j in range(int(np.log2(N))):
            y = (y << 1) | (x & 1)
            x >>= 1
        reversed_arr[y] = arr[i]
    return reversed_arr

def fast_fourier_transform(x):
    N = len(x)
    logN = int(np.log2(N))
    x = bit_reverse(x)
    h = 1
    
    while h < N:
        step = 2*h
        phase_factor = np.exp(-2j*np.pi / step) #phase factor to shift phases on the unit circle
        for i in range(0, N, step):
            w = 1.0 + 0j #initalize starting phase step
            for k in range(i,i+h): #do butterfly loop
                a = x[k]
                b = phase_factor * x[k + h] 
                x[k] = a + b # high frequences
                x[k + h] = a - b  # low frequencies
                w *= phase_factor #shift to the next phase on the i unit circle
        h *= 2 # group by increasing  by powers of 2 
    return x


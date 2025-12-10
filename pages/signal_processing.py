import streamlit as st
import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def binaryInversionTable(N):

    b = [0]*N

    i = 1
    while i < N:

        for j in range(i):

            b[i + j] = b[j] + N // (2 * i)

        i *= 2

    return b


def primitiveRootOfUnity(stage):

    powers = []

    order = 2**stage
    m = order // 2

    angle = -2 * np.pi / order
    W = np.exp(1j * angle)

    current = 1 + 0j


    for i in range(m):
        powers.append(current)
        current *= W

    return np.array(powers)

    
def fft(arr):

    f = np.array(arr, dtype = complex)

    N = len(f)
    n = int(math.log2(N))

    b = np.array(binaryInversionTable(N))

    for j in range(N):
        if j < b[j]:
            f[j], f[b[j]] = f[b[j]], f[j]

    x = f.copy()
    y = np.zeros(N, dtype = complex)

    
    for stage in range(1, n + 1):

        block_size = 2**stage
        half_block = block_size // 2

        W = primitiveRootOfUnity(stage)

        block = 0
        while block < N:

            for k in range(half_block):
                u = x[block + k]
                v = x[block + k + half_block] * W[k]

                y[block + k] = u + v
                y[block + k + half_block] = u - v
            block += block_size

        x = y.copy()

    return x


def fft_shift(transform):

    height, width = transform.shape
    height2 = height // 2
    width2 = width // 2
    
    centered = np.zeros_like(transform)

    centered[:height2, :width2] = transform[height2:, width2:]
    centered[:height2, width2:] = transform[height2:, :width2]
    centered[height2:, :width2] = transform[:height2, width2:]
    centered[height2:, width2:] = transform[:height2, :width2]

    return centered


def fft_2d(img_matrix):

    height, width = img_matrix.shape


    row_transform = np.zeros((height, width), dtype = complex)
    
    for r in range(height):
        row_transform[r, :] = fft(img_matrix[r, :])

    transform = np.zeros((height, width), dtype = complex)

    for c in range(width):
        transform[:, c] = fft(row_transform[:, c])

    return fft_shift(transform)




def main():


    st.set_page_config(layout = "centered")
    st.set_page_config(initial_sidebar_state = "collapsed")


    uploaded_file = st.file_uploader("Upload an image (dimensions must be power of 2)", type=["png","jpg","jpeg"])


    if uploaded_file:
        img = Image.open(uploaded_file).convert("L")
        img_matrix = np.array(img, dtype = float)
        height, width = img_matrix.shape

        if (height != width) or (height & (height - 1) != 0) or (width & (width - 1) != 0):
            st.error("Height and Width of image must be powers of two and equal")
        else:
            img_matrix = img_matrix / 255.0

        left_side, right_side = st.columns([1, 1,])

        with left_side:
            left, right = st.columns([1, 1])

            with left:
                st.image(img_matrix, caption = "Image", use_container_width = True)
            
            with right:
                img_matrix1 = img_matrix.copy()
                result = fft_2d(img_matrix1)

                magnitude = np.log1p(np.abs(result))

                
                fig, ax = plt.subplots()
                ax.imshow(magnitude, cmap = 'gray')
                ax.axis('off')
                st.pyplot(fig)

        with right_side:
            img_matrix2 = img_matrix.copy()
            F = fft_2d(img_matrix2)
            magnitude = np.log1p(np.abs(F))

            height, width = magnitude.shape
            x = np.arange(width)
            y = np.arange(height)
            X, Y = np.meshgrid(x, y)

            fig = plt.figure(figsize=(6,6))
            ax = fig.add_subplot(111, projection="3d")
            ax.plot_surface(X, Y, magnitude, cmap="viridis")
            st.pyplot(fig)








if __name__ == "__main__":
    main()


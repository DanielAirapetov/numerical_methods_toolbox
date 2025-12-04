import streamlit as st
import pandas as pd
import numpy as np
import os, sys


# Add project ROOT so imports work
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from sections.linear_systems.direct_elimination.gaussian import frankieG, markG, danielG
from sections.linear_systems.direct_elimination.gauss_jordan import frankieGJ, markGJ, danielGJ
from sections.linear_systems.iterative.seidel import frankieGS, danielGS, markGS, jhonGS
from sections.linear_systems.iterative.jacobi import frankieJ, danielJ, markJ, jhonJ


def printResults(results, method, member):
    st.write(f"{method} results using {member}'s function:")
    for i, value in enumerate(results):
        st.write(f"x{i+1} = {value}")


def createMatrix():
    # Initialize session state
    if "rows" not in st.session_state:
        st.session_state.rows = 3
    if "cols" not in st.session_state:
        st.session_state.cols = 4

    # Build table from current sizes
    default_df = pd.DataFrame(
        [[0] * st.session_state.cols for _ in range(st.session_state.rows)]
    )

    edited_df = st.data_editor(default_df, key="matrix_editor")

    # Controls BELOW the table
    col1, col2 = st.columns(2)
    with col1:
        new_rows = st.number_input(
            "Rows", min_value=1, max_value=10,
            value=st.session_state.rows, key="rows_input"
        )
    with col2:
        new_cols = st.number_input(
            "Columns", min_value=1, max_value=10,
            value=st.session_state.cols, key="cols_input"
        )

    # If user changes rows/cols → update state and rerun
    if new_rows != st.session_state.rows or new_cols != st.session_state.cols:
        st.session_state.rows = new_rows
        st.session_state.cols = new_cols
        st.rerun()   # rebuild the table with new shape

    return edited_df.to_numpy(float)


def getMatrix(input_type):
    if input_type == "GUI":
        return createMatrix()
    else:  # CSV
        uploaded = st.file_uploader("Upload augmented matrix as CSV", type="csv")
        if uploaded is None:
            st.info("Please upload a CSV file to continue.")
            return None
        df = pd.read_csv(uploaded, header=None)
        return df.to_numpy(dtype=float)         


def selectMember():
    return st.selectbox("Select whose method to use:", ["Daniel", "Francis", "Jhon", "Mark"])


def main():
    st.title("Systems of Equations Methods Calculator")
    method_type = st.selectbox("Choose a method type:", ["Direct", "Iterative"])

    if method_type == "Direct":
        method = st.selectbox("Choose a method:", ["Gaussian", "Gauss-Jordan"])
        input_type = st.selectbox("Choose a input type: ", ["GUI","CSV"])
        matrix = getMatrix(input_type)
        member = selectMember()

        if st.button("Solve Direct"):
            if matrix is None:
                st.error("Please provide a matrix first.")
            else:
                results = None

                if member == "Francis":
                    if method == "Gaussian":
                        reduced = frankieG.gauss_elim(matrix.copy())
                        results = frankieG.back_sub(reduced)
                    else:  # Gauss-Jordan
                        results = frankieGJ.GJ_elim(matrix.copy())

                elif member == "Mark":
                    if method == "Gaussian":
                        results = markG.gaussianEliminationMethod(matrix.copy())
                    else:  # Gauss-Jordan
                        results = markGJ.gaussJordanElimination(matrix.copy())

                elif member == "Daniel":
                    list = matrix.tolist()
                    if method == "Gaussian":
                        results = danielG.gaussian_elimination(list)
                    else:  # Gauss-Jordan
                        results = danielGJ.gauss_jordan_elimination(list)

                else:
                    st.error("Still dont have jhons direct elim functions")
                        
                if results is not None:
                    printResults(results, method, member)

    else:  # Iterative
        method = st.selectbox("Choose a method:", ["Gauss-Seidel", "Jacobi"])
        input_type = st.selectbox("Choose an input type: ", ["GUI", "CSV"])
        matrix = getMatrix(input_type)
        member = selectMember()

        if st.button("Solve Iterative"):
            if matrix is None:
                st.error("Please provide a matrix first.")
            else:
                initial = np.zeros(matrix.shape[0])
                tolerance = 0.001
                flag = 4

                results = None
                iters = None

                if member == "Francis":
                    if method == "Gauss-Seidel":
                        results, iters = frankieGS.GaussSiedel(matrix, initial, tolerance, flag)
                    else:  # Jacobi
                        results, iters = frankieJ.Jacobi(matrix, initial, tolerance, flag)

                elif member == "Daniel":
                    list = matrix.tolist()
                    if method == "Gauss-Seidel":
                        results, iters = danielGS.gauss_seidel_iterative_method(list, tolerance, flag)
                    else:  # Jacobi
                        results, iters = danielJ.jacobi_iterative_method(list, tolerance, flag)

                elif member == "Mark":
                    if method == "Gauss-Seidel":
                        results, iters = markGS.gaussSeidelMethod(matrix, tolerance, flag)
                    else:
                        results, iters = markJ.gaussSeidelMethod(matrix, tolerance, flag)
                else: #Jhon
                    if method == "Gauss-Seidel":
                        results, iters = jhonGS.gauss_seidel(matrix,tolerance,flag)
                    else:
                        results, iters = jhonJ.jacobi_method(matrix,tolerance,flag)
        
                if results is not None:
                    printResults(results, method, member)
                    if iters is not None:
                        st.write("Iterations:", iters)

if __name__ == "__main__":
    main()
    
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
from sections.linear_systems.iterative.seidel import frankieGS, danielGS
from sections.linear_systems.iterative.jacobi import frankieJ, danielJ

def printResults(results, method, member):
    st.write(f"{method} results using {member}'s function:")
    for i, value in enumerate(results):
        st.write(f"x{i+1} = {value}")

def createMatrix():
    rows = st.number_input("Rows", 1, 10, 3)
    cols = st.number_input("Columns", 1, 10, 4)
    st.write("Enter your augmented matrix:")
    default_df = pd.DataFrame([[0]*int(cols) for _ in range(int(rows))])
    edited_df = st.data_editor(default_df)
    return edited_df.to_numpy(dtype=float)

def getMatrix(input_type):
    if input_type == "CSV":
        uploaded = st.file_uploader("Upload augmented matrix as CSV", type="csv")
        if uploaded is None:
            st.info("Please upload a CSV file to continue.")
            return None
        df = pd.read_csv(uploaded, header=None)
        return df.to_numpy(dtype=float)
    else:  # GUI
        return createMatrix()
    
    
def selectMember():
    return st.selectbox("Select whose method to use:", ["Daniel", "Francis", "Jhon", "Mark"])

st.title("Systems of Equations Methods Calculator")
method_type = st.selectbox("Choose a method type:", ["Direct", "Iterative"])

if method_type == "Direct":
    method = st.selectbox("Choose a method:", ["Gaussian", "Gauss-Jordan"])
    input_type = st.selectbox("Choose a input type: ", ["CSV", "GUI"])
    matrix = getMatrix(input_type)
    member = selectMember()

    if st.button("Solve Direct"):
        if member == "Francis":
            reduced = frankieG.gauss_elim(matrix.copy())
            resultsG = frankieG.back_sub(reduced)
            resultsGJ = frankieGJ.GJ_elim(matrix.copy())
            printResults(resultsG if method == "Gaussian" else resultsGJ, method, member)

        elif member == "Mark":
            resultsG = markG.gaussianEliminationMethod(matrix.copy())
            resultsGJ = markGJ.gaussJordanElimination(matrix.copy())
            printResults(resultsG if method == "Gaussian" else resultsGJ, method, member)

        elif member == "Daniel":
            resultsG = danielG.gaussian_elimination(matrix.copy())
            resultsGJ = danielGJ.gauss_jordan_elimination(matrix.copy())
            printResults(resultsG if method == "Gaussian" else resultsGJ, method, member)

        else:
            st.error("Jhon's methods not implemented yet.")

else:  # Iterative
    method = st.selectbox("Choose a method:", ["Gauss-Seidel", "Jacobi"])
    input_type = st.selectbox("Choose an input type: ", ["CSV", "GUI"])
    matrix = getMatrix(input_type)
    member = selectMember()

    if st.button("Solve Iterative"):
        initial = np.zeros(matrix.shape[0])
        tolerance = 0.001
        flag = 4

        if member == "Francis":
            resultsGS, i = frankieGS.GaussSiedel(matrix, initial, tolerance, flag)
            resultsJ, _ = frankieJ.Jacobi(matrix, initial, tolerance, flag)
            printResults(resultsGS if method == "Gauss-Seidel" else resultsJ, method, member)
            st.write("Iterations:", i)

        elif member == "Daniel":
            resultsGS, i = danielGS.gauss_seidel_iterative_method(matrix, tolerance, flag)
            resultsJ, _ = danielJ.jacobi_iterative_method(matrix, tolerance, flag)
            printResults(resultsGS if method == "Gauss-Seidel" else resultsJ, method, member)

        else:
            st.error("Mark and Jhon's iterative methods not implemented yet.")
            
import streamlit as st
import pandas as pd
import numpy as np
from sections.linear_systems.direct_elimination.gaussian import frankieG, markG, danielG, jhonG
from sections.linear_systems.direct_elimination.gauss_jordan import frankieGJ, markGJ, danielGJ, jhonGJ



def printResults(results):
    for i, value in enumerate(results):
        st.write(f"x{i+1} = {value}")

st.title("Directed Elimination Methods Calculator: ")
method = st.selectbox("Choose a method: ", ["Gaussian", "Gauss-Jordan"])

rows = st.number_input("Rows", 1, 10, 3)
cols = st.number_input("Columns", 1, 10, 4)

st.write("Enter your augmented matrix: ")

default_df = pd.DataFrame([[0]*int(cols) for _ in range(int(rows))])

edited_df = st.data_editor(default_df)

matrix = edited_df.to_numpy(dtype=float)
members = ["Daniel", "Francis","Jhon", "Mark"]
member = st.selectbox("Select group members function to use: ", members)

if member == "Francis":
    reducedmat = frankieG.gauss_elim(matrix)
    resultsG = frankieG.back_sub(reducedmat)
    resultsGJ = frankieGJ.GJ_elim(matrix)
    if method == "Gaussian":
        printResults(resultsG)
    else:
        printResults(resultsGJ)

elif member == "Mark":
    resultsG = markG.gaussianEliminationMethod(matrix)
    resultsGJ = markGJ.gaussJordanElimination(matrix)
    if method == "Gaussian":
        printResults(resultsG)
    else:
        printResults(resultsGJ)
  
elif member == "Daniel":
    resultsG = danielG.gaussian_elimination(matrix)
    resultsGJ = danielGJ.gauss_jordan_elimination(matrix)
    if method == "Gaussian":
        printResults(resultsG)
    else:
        printResults(resultsGJ)

else:
    st.write("Still dont have Jhons function")
    




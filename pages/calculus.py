import streamlit as st
import pandas as pd
import numpy as np
import os, sys

# Add project ROOT so imports work
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from sections.calculus.differentiation import danielD, frankyD, markD, jhonD
from sections.calculus.integration.simpson import danielS, frankyS, markS, jhonS
from sections.calculus.integration.trapezoid import danielT, frankyT, markT, jhonT

# functions should be inputed via a table, graphically displays as a scatterplot

def createTable():
    # Initialize default session state
    if "rows" not in st.session_state: # 2: one-sided derivative or trapezoid, 3: centered derivative or simpsons
        st.session_state.min_rows = 3
    columns = 2


def getTable(input_type, operation_type):
    if input_type == "GUI":
        return createTable()
    elif input_type == "CSV":
        uploaded = st.file_uploader("Upload augmented matrix as CSV", type="csv")
        if uploaded is None:
            st.info("Please upload a CSV file to continue.")
            return None
        df = pd.read_csv(uploaded, header=None)
        return df.to_numpy(dtype=float)  

def selectMember():
    return st.selectbox("Select whose method to use:", ["Daniel", "Francis", "Jhon", "Mark"])

st.title("Calculus Calculator")
operation = st.selectbox("Choose an operation:", ["Differentiation", "Integration"])

if operation == "Differentiation":
    input_type = st.selectbox("Choose a input type: ", ["CSV", "GUI"])
    table = getTable(input_type)
    member = selectMember()
    

elif operation == "Integration":
    method = st.selectbox("Choose a method:", ["Simpson", "Trapezoid"])
    if method == "Simpson":
        input_type = st.selectbox("Choose a input type: ", ["CSV", "GUI"])
        table = getTable(input_type, method)
        member = selectMember()


    elif method == "Trapezoid":
        input_type = st.selectbox("Choose a input type: ", ["CSV", "GUI"])
        table = getTable(input_type, method)
        member = selectMember()


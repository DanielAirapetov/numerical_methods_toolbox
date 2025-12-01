import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def user_corrected_equation(equation_str):
    math_functions = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', "pow" ]
    for funcion in math_functions:
        equation_str = equation_str.replace(funcion, f'np.{funcion}')
    return equation_str

def evaluate_function(corrected_equation_str, x_value):
    return eval(corrected_equation_str, {"np": np, "x": x_value})

def main():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 20px !important;
            }
            .title {
                text-align: center !important;
            }
            .subtitle {
                text-align: center !important;
                margin-top: 20px !important;
                margin-bottom: 20px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<h1 class="title">Solving Nonlinear Equations</h1>', unsafe_allow_html=True)
    equation = None
    equation = st.text_input("Enter the equation you want to solve: ")
    corrected_equation = None
    if equation != None and equation != "":
        corrected_equation= user_corrected_equation(equation)  
        # Plotting the function
        x = np.linspace(-10, 10, 1600)
        y = evaluate_function(corrected_equation, x)
        fig, ax = plt.subplots(figsize=(20, 20))

        # Plot
        ax.plot(x, y, color='red', linewidth=2)

        # Center axes
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Ticks
        ax.set_xticks(np.arange(-10, 11, 1))
        ax.set_yticks(np.arange(-10, 11, 1))
        ax.tick_params(length=5, width=1)

        # Grid
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

        # Limits
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)

        # Labels
        ax.set_title(f"f(x) = {equation}")

        st.pyplot(fig)
        plt.clf()


        
        method = st.selectbox("Select a root-finding method:", ["None", "Bisection Method", "False Position Method", "Secant Method", "Newton Method"])
        if method != "None":
            tolerance = st.number_input("Enter the tolerance level:", value = 1 * 10 ** -6, format="%.6f")
            flag = st.selectbox("Select a flag:", [1, 2, 3, 4])      
            if method == "Newton Method":
                initial_guess = st.number_input("Enter the initial x value:", value=0.0, format="%.4f")
            else:
                left_bound = st.number_input("Enter the left bound:", value=0.0, format="%.4f")
                right_bound = st.number_input("Enter the right bound:", value=0.0, format="%.4f")
    
    

main()

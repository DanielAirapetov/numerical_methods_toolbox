import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import plotly.express as px
import os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)
    
from sections.root_finding.bisection import mark_bisection
from sections.root_finding.bisection import jhon_bisection
from sections.root_finding.bisection import franky_bisection
from sections.root_finding.bisection import daniel_bisection

from sections.root_finding.false_position import mark_false_position
from sections.root_finding.false_position import jhon_false_position
from sections.root_finding.false_position import franky_false_position
from sections.root_finding.false_position import daniel_false_position

from sections.root_finding.secant import mark_secant
from sections.root_finding.secant import jhon_secant
from sections.root_finding.secant import franky_secant
from sections.root_finding.secant import daniel_secant

from sections.root_finding.newton import mark_newton
from sections.root_finding.newton import jhon_newton
from sections.root_finding.newton import daniel_newton

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
    
    if equation != None and equation != "":
        x_expression = sp.Symbol('x')
        expr = sp.sympify(equation) 
            
        function = sp.lambdify(x_expression, expr, "numpy")
        derivative_function = sp.lambdify(x_expression, sp.diff(expr, x_expression))
        
        x_graph = np.linspace(-10, 10, 1600)
        y_graph = function(x_graph)
        
        df = pd.DataFrame({"x": x_graph, "y": y_graph})
        
        fig = px.line(df, x = "x", y = "y", title=f"Graph of y = {equation}")
        
        fig.update_xaxes(range=[-10, 10], tick0=-10, dtick=1)
        fig.update_yaxes(range=[-10, 10], tick0=-10, dtick=1)
        
        st.plotly_chart(fig)
        
        method = st.selectbox("Select a root-finding method:", ["None", "Bisection Method", "False Position Method", "Secant Method", "Newton Method"])
        person = st.selectbox("Person:", ["None", "Mark", "Francis", "Daniel", "Jhon"])
        
        if method != "None" and person != "None":
            tolerance = st.number_input("Enter the tolerance level:", value = 1 * 10 ** -6, format="%.6f")
            flag = st.selectbox("Select a flag:", [1, 2, 3, 4])     
            
            if method == "Newton Method":
                initial_guess = st.number_input("Enter the initial x value:", value=0.0, format="%.4f")
                
                user_input_valid = False
                
                if derivative_function(initial_guess) != 0:
                    user_input_valid = True
                else:
                    st.error("The derivative at the initial guess cannot be zero. Please enter a valid initial guess.")
                    
                if user_input_valid:
                    if person == "Mark":
                        if st.button("Calculate Root"):
                            root, iterations = mark_newton.newtonMethod(initial_guess, tolerance, flag, expr)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Daniel":
                        if st.button("Calculate Root"):
                            root, iterations = daniel_newton.newton(initial_guess, tolerance, flag, expr)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Jhon":
                        if st.button("Calculate Root"):
                            root, iterations = jhon_newton.newton_method(initial_guess, tolerance, flag, expr)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                
            else:
                left_bound = st.number_input("Enter the left bound:", value=0.0, format="%.4f")
                right_bound = st.number_input("Enter the right bound:", value=0.0, format="%.4f")
                
                user_input_valid = False
                
                if method == "Bisection Method" or method == "False Position Method":
                    if function(left_bound) * function(right_bound) < 0:
                        user_input_valid = True
                    else:
                        st.error("The function must have different signs at the left and right bounds. Please enter valid bounds.")
                
                if method == "Bisection Method" and user_input_valid:
                    if person == "Mark":
                        if st.button("Calculate Root"):
                            root, iterations = mark_bisection.bisectionMethod(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Jhon":
                        if st.button("Calculate Root"):
                            root, iterations = jhon_bisection.bisection(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Francis":
                        if st.button("Calculate Root"):
                            root, iterations = franky_bisection.bisection(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    else:
                        if person == "Daniel":
                            if st.button("Calculate Root"):
                                root, iterations = daniel_bisection.bisection(left_bound, right_bound, tolerance, flag, function)
                                st.write(f"Root: {root}, Iterations: {iterations}")
                elif method == "False Position Method" and user_input_valid:
                    if person == "Mark":
                        if st.button("Calculate Root"):
                            root, iterations = mark_false_position.falsePositionMethod(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Jhon":
                        if st.button("Calculate Root"):
                            root, iterations = jhon_false_position.false_position_method(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Francis":
                        if st.button("Calculate Root"):
                            root, iterations = franky_false_position.regulafalsi(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    else:
                        if person == "Daniel":
                            if st.button("Calculate Root"):
                                root, iterations = daniel_false_position.falsePosition(left_bound, right_bound, tolerance, function)
                                st.write(f"Root: {root}, Iterations: {iterations}")
                elif method == "False Position Method" and user_input_valid:
                    if person == "Mark":
                        if st.button("Calculate Root"):
                            root, iterations = mark_false_position.falsePositionMethod(left_bound, right_bound, tolerance, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Jhon":
                        if st.button("Calculate Root"):
                            root, iterations = jhon_false_position.false_position_method(left_bound, right_bound, tolerance, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Francis":
                        if st.button("Calculate Root"):
                            root, iterations = franky_false_position.regulafalsi(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    else:
                        if person == "Daniel":
                            if st.button("Calculate Root"):
                                root, iterations = daniel_false_position.falsePosition(left_bound, right_bound, tolerance, flag, function)
                                st.write(f"Root: {root}, Iterations: {iterations}")
                elif method == "Secant Method":
                    if person == "Mark":
                        if st.button("Calculate Root"):
                            root, iterations = mark_secant.secantMethod(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Jhon":
                        if st.button("Calculate Root"):
                            root, iterations = jhon_secant.secant_method(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    elif person == "Francis":
                        if st.button("Calculate Root"):
                            root, iterations = franky_secant.secant(left_bound, right_bound, tolerance, flag, function)
                            st.write(f"Root: {root}, Iterations: {iterations}")
                    else:
                        if person == "Daniel":
                            if st.button("Calculate Root"):
                                root, iterations = daniel_secant.secant(left_bound, right_bound, tolerance, flag, function)
                                st.write(f"Root: {root}, Iterations: {iterations}")
main()


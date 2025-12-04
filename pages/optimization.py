import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sympy as sp
import os, sys


ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from sections.optimization.members import daniel, jhon, mark, francis

def safe_eval(func: str, x):
    allowed = {
        "x": x,
        "np": np,
        "sin": np.sin, "cos": np.cos, "tan": np.tan,
        "exp": np.exp, "log": np.log,
        "sqrt": np.sqrt, "abs": np.abs,
        "pi": np.pi, "e": np.e
    }
    return eval(func, {"__builtins__": {}}, allowed)

def float_input(label, default, key):
    text = st.text_input(label, value=str(default), key = key)
    try:
        return float(text)
    except ValueError:
        return None




def main():

    if "compute_goldenSection" not in st.session_state:
        st.session_state["compute_goldenSection"] = False
    if "compute_newtonMinMax" not in st.session_state:
        st.session_state["compute_newtonMinMax"] = False
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = None
    if "outputs" not in st.session_state:
        st.session_state["outputs"] = None




    # set page layout to wide
    st.set_page_config(layout="wide")

    # set the title with some html for centering and margins
    st.markdown("<h1 style='text-align:center; margin-bottom:10px; margin-top:-30px'>Optimization Methods</h1>",unsafe_allow_html=True)

    # used to safely evaluate an inputed function







    # center the layout
    # add blank space on left and right
    # center the plots and input
    left, center_left, center_right, right = st.columns([1, 4, 4, 1])


    # right side of page
    # inputs and selections
    with center_right:

        st.write("## Enter a Function")
        function_text = st.text_input("f(x) =", value="")
        
        if function_text.strip():

                try:

                    function_symbolic = sp.sympify(function_text, locals = {
                        "sin": sp.sin,
                        "cos": sp.cos,
                        "tan": sp.tan,
                        "log": sp.log,
                        "exp": sp.exp,
                        "sqrt": sp.sqrt,
                        "pi": sp.pi,
                        "e": sp.E,
                        })

                except Exception as e:

                    function_symbolic = None

                    st.error(f"Error parsing function: {e}")
        else:
            function_symbolic = None

        # check if the symbolic function has a log in it
        # need to make sure user doesn't input anything less than or equal to 0 for the bounds
        if function_symbolic != None and function_symbolic.has(sp.log):
            contains_log = True
        else:
            contains_log = False




        method_col, member_col, delta_col = st.columns([0.9, 0.9, 1])

        with method_col:
            method = st.selectbox(
                "Choose a method",
                options = ["Golden Section", "Newton Min/Max"]
                )
        with member_col:
            member = st.selectbox(
                    "Choose a member",
                    options = ["Daniel", "Jhon", "Mark", "Francis"]
                    )
        with delta_col:
            delta = float_input("Error threshold", "", key= "delta_key")
            invalid_delta = False
            if delta != None and delta <= 0:
                invalid_delta = True
                st.error("Error threshold must be greater than 0")



        
        if method == "Golden Section":

            st.markdown("<p style='margin-bottom:-10px;'>Choose bounds that bracket a min/max</p>", unsafe_allow_html=True)

            input_box1, input_box2 = st.columns(2)

            with input_box1:
                left_bound = float_input("a: ", "", key = "left_bound_key")
            with input_box2:
                right_bound = float_input("b: ", "", key = "right_bound_key")

            invalid_bound = False
            if contains_log:
                if left_bound != None and left_bound <= 0:
                    st.error("a: log(x) is undefined for values less than or equal to 0")
                    invalid_bound = True
                if right_bound != None and right_bound <= 0:
                    st.error("b: log(x) is undefined for values less than or equal to 0")
                    invalid_bound = True

            min_max = st.segmented_control(
                    "",
                    options = ["Minimum", "Maximum"],
                    default = "Minimum"
            )
            if min_max == "Minimum":
                flag = 1
            else:
                flag = 2

        else:
            left_bound = float_input("Initial Guess: ", "", key = "left_bound_key")
            
            invalid_bound = False
            if left_bound != None and left_bound <= 0:
                st.error("log(x) is undefined for values less than or equal to 0")
                invalid_bound = True


        compute_button, computed_result = st.columns([1, 1])

        
        with compute_button:

            disable_compute = invalid_bound or invalid_delta
            if st.button("Compute", disabled = invalid_bound or invalid_delta):
                if function_text.strip() != "" and delta != None:
                    if method == "Golden Section" and left_bound != None and right_bound != None:
                        st.session_state["compute_goldenSection"] = True
                        st.session_state["compute_newtonMinMax"] = False
                        
                        st.session_state["inputs"] = {
                                "a": left_bound,
                                "b": right_bound,
                                "delta": delta,
                                "flag": flag,
                                "method": "golden",
                                "member": member,
                                "func": function_symbolic
                                }
                    elif method == "Newton Min/Max" and left_bound != None:
                        st.session_state["compute_goldenSection"] = False
                        st.session_state["compute_newtonMinMax"] = True

                        st.session_state["inputs"] = {
                                "a": left_bound,
                                "delta": delta,
                                "method": "newton",
                                "member": member,
                                "func": function_symbolic
                                }




        with computed_result:

            if st.session_state.get("compute_goldenSection", False):

                inputs = st.session_state["inputs"]
                st.session_state["compute_goldenSection"] = False

                if member == "Daniel":
                    result, iterations = daniel.goldenSectionMethod(inputs["a"], inputs["b"], inputs["delta"], inputs["flag"], inputs["func"])
                elif member == "Jhon":
                    result, iterations = jhon.goldenSectionMethod(inputs["a"], inputs["b"], inputs["delta"], inputs["flag"], inputs["func"])
                elif member == "Mark":
                    result, iterations = mark.goldenSectionMethod(inputs["a"], inputs["b"], inputs["delta"], inputs["flag"], inputs["func"])
                elif member == "Francis":
                    result, iterations = francis.goldenSectionMethod(inputs["a"], inputs["b"], inputs["delta"], inputs["flag"], inputs["func"])

                st.session_state["outputs"] = (result, iterations)

            elif st.session_state.get("compute_newtonMinMax", False):

                inputs = st.session_state["inputs"]
                st.session_state["compute_newtonMinMax"] = False

                if member == "Daniel":
                    result, iterations = daniel.newtonMinMaxMethod(inputs["a"], inputs["delta"], inputs["func"])
                elif member == "Jhon":
                    result, iterations = jhon.newtonMinMaxMethod(inputs["a"], inputs["delta"], inputs["func"])
                elif member == "Mark":
                    result, iterations = mark.newtonMinMaxMethod(inputs["a"], inputs["delta"], inputs["func"])
                elif member == "Francis":
                    result, iterations = francis.newtonMinMaxMethod(inputs["a"], inputs["delta"], inputs["func"])

                st.session_state["outputs"] = (result, iterations)

            if st.session_state.get("outputs", False) != None:
                result, iterations = st.session_state["outputs"]
                st.write(f"**Result:** {result}")
                st.write(f"**Iterations:** {iterations}")




    # plot with interval bound inputs to increase or decrease the viewing window of the plotted function
    with center_left:

        # plot
        x_points = np.linspace(-10, 10, 500)   # temporary defaults (will be overwritten)
        y_points = np.full_like(x_points, np.nan)

        
        data = pd.DataFrame({"x": x_points, "f(x)": y_points})

        plot_placeholder = st.empty()

        left_interval, right_interval = st.columns([1, 1])


        with left_interval:
            a = st.number_input(
                "Left Bound",
                value = -5.0,
                step=0.1,
            )

            if contains_log and a <= 0:
                a = st.number_input(
                        "Left Bound",
                        value = 0.01,
                        step = 0.1,
                        )

        with right_interval:
            b = st.number_input(
                "Right Bound",
                value=5.0,
                step=0.1,
            )

            if contains_log and b <= 0:
                b = st.number_input(
                        "Right Bound",
                        value = 0.01,
                        step = 0.1,
                        )

        # recompute the plot using bounds entered by user
        x_points = np.linspace(a, b, 500)
        y_points = np.full_like(x_points, np.nan)

        if function_text.strip() != "":
            try:
                y_points = safe_eval(function_text, x_points)
            except Exception as e:
                plot_placeholder.error(f"Error evaluating function: {e}")

        data = pd.DataFrame({"x": x_points, "f(x)": y_points})

        # Determine y-range
        if not np.isnan(y_points).all():
            y_min = np.nanmin(y_points)
            y_max = np.nanmax(y_points)
        else:
            y_min, y_max = -10, 10

        # Create Plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_points, y=y_points, mode="lines", name="f(x)"))

        fig.update_layout(
            width=600,
            height=600,
            xaxis=dict(title="x", range=[a, b]),
            yaxis=dict(title="f(x)", range=[y_min, y_max]),
            showlegend=False,
        )

        fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor="gray", dtick = 1)
        fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor="gray", dtick = 1)

        # Render Plotly chart
        plot_placeholder.plotly_chart(fig, use_container_width=False)


if __name__ == "__main__":
    main()

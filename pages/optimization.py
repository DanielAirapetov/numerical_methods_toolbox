import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import sympy as sp
import os, sys


ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from sections.optimization.members import daniel, jhon, mark, francis

# set page layout to wide
st.set_page_config(layout="wide")

# set the title with some html for centering and margins
st.markdown("<h1 style='text-align:center; margin-bottom:10px; margin-top:-30px'>Optimization Methods</h1>",unsafe_allow_html=True)

# used to safely evaluate an inputed function
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

def float_input(label, default):
    text = st.text_input(label, value=str(default))
    try:
        return float(text)
    except ValueError:
        return None







# center the layout
# add blank space on left and right
# center the plots and input
left, center_left, center_right, right = st.columns([1, 4, 4, 1])


# right side of page
# inputs and selections
with center_right:

    st.write("## Enter a Function")
    function_text = st.text_input("f(x) =", value="")
    

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
        delta = float_input("Error threshold", "")

    if method == "Golden Section":

        st.markdown("<p style='margin-bottom:-10px;'>Choose bounds that bracket a min/max</p>", unsafe_allow_html=True)

        input_box1, input_box2 = st.columns(2)
        with input_box1:
            #left_bound = st.number_input("a: ", value=0.0, format="%f")
            left_bound = float_input("a: ", "")
        with input_box2:
            #right_bound = st.number_input("b: ", value=0.0, format="%f")
            right_bound = float_input("b: ", "")

        min_max = st.segmented_control(
                "",
                options = ["Minimum", "Maximum"],
                default = "Minimum"
        )

    else:
        left_bound = st.number_input("Initial Guess", value=0, format="%f")


    compute_button, computed_result = st.columns([1, 1])

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


    with compute_button:

        if st.button("Compute") and function_text.strip != "" and delta != None and left_bound != None and right_bound != None:

            if method == "Golden Section":

                st.session_state["compute_goldenSection"] = True
            else:

                st.session_state["compute_newtonMinMax"] = True


    with computed_result:

        if min_max == "Minimum":
            flag = 1
        else:
            flag = 2

        if st.session_state.get("compute_goldenSection", False):
            if member == "Daniel":
                result, iterations = daniel.goldenSectionMethod(left_bound, right_bound, 0.000001, flag, function_symbolic)
            elif member == "Jhon":
                result, iterations = jhon.goldenSectionMethod(left_bound, right_bound, 0.000001, flag, function_symbolic)
            elif member == "Mark":
                result, iterations = mark.goldenSectionMethod(left_bound, right_bound, 0.000001, flag, function_symbolic)
            elif member == "Francis":
                result, iterations = francis.goldenSectionMethod(left_bound, right_bound, 0.000001, flag, function_symbolic)

            st.write(f"**{min_max} at:** {result}")
            st.write(f"**Iterations:** {iterations}")


# plot with interval bound inputs to increase or decrease the viewing window of the plotted function
with center_left:

    # plot
    x_points = np.linspace(-10, 10, 500)   # temporary defaults (will be overwritten)
    y_points = np.full_like(x_points, np.nan)

    
    df = pd.DataFrame({"x": x_points, "f(x)": y_points})

    plot_placeholder = st.empty()

    left_interval, right_interval = st.columns([1, 1])


    with left_interval:
        a = st.number_input(
            "Left Bound",
            value=-10.0,
            step=0.1,
            key="left_bound"
        )

    with right_interval:
        b = st.number_input(
            "Right Bound",
            value=10.0,
            step=0.1,
            key="right_bound"
        )

    # recompute the plot using bounds entered by user
    x_points = np.linspace(a, b, 500)
    y_points = np.full_like(x_points, np.nan)

    if function_text.strip() != "":
        try:
            y_points = safe_eval(function_text, x_points)
        except Exception as e:
            plot_placeholder.error(f"Error evaluating function: {e}")

    df = pd.DataFrame({"x": x_points, "f(x)": y_points})

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("x", title="x", scale=alt.Scale(domain=[a, b])),
            y=alt.Y("f(x)", title="f(x)", scale=alt.Scale(domain=[np.nanmin(y_points), np.nanmax(y_points)] if not np.isnan(y_points).all() else [-10, 10])
                    )
            ).properties(width=600, height=600)
        )

    # render plot
    plot_placeholder.altair_chart(chart, use_container_width=False)

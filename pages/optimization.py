import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import sympy as sp
import os, sys

st.set_page_config(
    page_title ="Optimization",
    initial_sidebar_state ="collapsed" 
)

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from sections.optimization.members import daniel, jhon, mark, francis




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
        delta = float_input("Error threshold", "")



    
    if method == "Golden Section":

        st.markdown("<p style='margin-bottom:-10px;'>Choose bounds that bracket a min/max</p>", unsafe_allow_html=True)

        input_box1, input_box2 = st.columns(2)

        with input_box1:
            left_bound = float_input("a: ", "")
        with input_box2:
            right_bound = float_input("b: ", "")

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
        left_bound = float_input("Initial Guess: ", "")


    compute_button, computed_result = st.columns([1, 1])

    
    with compute_button:

        if st.button("Compute"):
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
            key="left_bound"
        )

    with right_interval:
        b = st.number_input(
            "Right Bound",
            value=5.0,
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

    data = pd.DataFrame({"x": x_points, "f(x)": y_points})

    chart = (
        alt.Chart(data)
        .mark_line()
        .encode(
            x=alt.X("x", title="x", scale=alt.Scale(domain=[a, b])),
            y=alt.Y("f(x)", title="f(x)", scale=alt.Scale(domain=[np.nanmin(y_points), np.nanmax(y_points)] if not np.isnan(y_points).all() else [-10, 10])
                    )
            ).properties(width=600, height=600)
        )

    # render plot
    plot_placeholder.altair_chart(chart, use_container_width=False)



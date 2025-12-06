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

# set_min and set_max are helper functions used to set the session_state of the min and max buttons for the golden section method
def set_min():
    st.session_state["minmax"] = "Minimum"

def set_max():
    st.session_state["minmax"] = "Maximum"






def main():


    # remove padding from top of page
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True
                )





    st.set_page_config(layout="wide")

    if "compute_goldenSection" not in st.session_state:
        st.session_state["compute_goldenSection"] = False
    if "compute_newtonMinMax" not in st.session_state:
        st.session_state["compute_newtonMinMax"] = False
    if "inputs" not in st.session_state:
        st.session_state["inputs"] = None
    if "outputs" not in st.session_state:
        st.session_state["outputs"] = None
    if "minmax" not in st.session_state:
        st.session_state["minmax"] = "Minimum"



    st.divider()

    left, center, right = st.columns([1, 3, 1])


    with left:
        with st.container():
            st.markdown("<div class = 'lower-button'>", unsafe_allow_html = True)
            if st.button("Back"):
                st.switch_page("app.py")
            st.markdown("</div>", unsafe_allow_html = True)
            

    with center:
        # set the title with some html for centering and margins
        st.markdown("<h1 style='text-align:center; margin-bottom:-20px; margin-top:20px'>Optimization Methods</h1>",unsafe_allow_html=True)

    st.divider()


    # add blank space on left and right
    # center the plots and input
    left, center_left, center_right, right = st.columns([1, 5, 4, 1])


    # right side of page
    # inputs and selections
    with center_right:

        st.markdown("<div style='height:100px'></div>", unsafe_allow_html=True)

        st.write("## Enter a Function")

        # when a new function is entered reset this before checking again
        discontinuous = False
        

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


            invalid_bound_a = False
            invalid_bound_b = False

            with input_box1:
                left_bound = float_input("a: ", "", key = "left_bound_key")
                if contains_log and left_bound != None:
                    if left_bound <= 0:
                        invalid_bound_a = True
                        st.error("a: log(x) not defined for x <= 0")
            with input_box2:
                right_bound = float_input("b: ", "", key = "right_bound_key")
                if contains_log and right_bound != None:
                    if right_bound <= 0:
                        invalid_bound_b = True
                        st.error("b: log(x) not defined for x <= 0")


            min_col, mid_space, max_col = st.columns([1, 0.001, 1])

            if "minmax" not in st.session_state:
                    st.session_state["minmax"] = "Minimum"



            with min_col:
                st.button(
                        "Minimum",
                        on_click = set_min,
                        type = "primary" if st.session_state["minmax"] == "Minimum" else "secondary",
                        use_container_width = True
                        )

            with max_col:
                st.button(
                        "Maximum",
                        on_click = set_max,
                        type = "primary" if st.session_state["minmax"] == "Maximum" else "secondary",
                        use_container_width = True
                        )

            # use it like before
            min_max = st.session_state["minmax"]
            flag = 1 if min_max == "Minimum" else 2


        else:

            invalid_bound_a = False
            invalid_bound_b = False



            left_bound = float_input("Initial Guess: ", "", key = "left_bound_key")

            if contains_log and left_bound != None:
                if left_bound <= 0:
                    invalid_bound_a = True
                    invalid_bound_b = True
                    st.error("log(x) not defined for x <= 0")




        compute_button, mid_space2, computed_result = st.columns([1, 0.001, 1])
        

        with compute_button:

            
            disable_compute =  invalid_bound_a or invalid_bound_b or invalid_delta or discontinuous


            if st.button("Compute", disabled = disable_compute, use_container_width = True):

                if function_symbolic != None and function_symbolic != 0 and delta != None:

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




    # plotly plot with interval bounds as text inputs which are converted to floats in order to allow the user to change the bounds of the function
    with center_left:

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        # plot
        x_points = np.linspace(-10, 10, 500)   # temporary defaults (will be overwritten)
        y_points = np.full_like(x_points, np.nan)

        
        data = pd.DataFrame({"x": x_points, "f(x)": y_points})

        plot_placeholder = st.empty()

        left_space, left_interval, right_interval, right_space = st.columns([0.01, 2, 2, 1])


        with left_interval:
            a = float_input("Left Bound", -5.00, key = "left_interval_key")
            if contains_log and a != None:
                if a <= 0:
                    st.error("log(x) not defined for x <= 0. Change bound to plot function.")
        with right_interval:
            b = float_input("Right Bound", 5.00, key = "right_interval_key")
            if contains_log and b != None:
                if b <= 0:
                    st.error("log(x) not defined for x <= 0. Change bound to plot function.")


        # recompute the plot using bounds entered by user
        if a != None and b != None:
            x_points = np.linspace(a, b, 500)
            y_points = np.full_like(x_points, np.nan)

        if function_text.strip() != "":
            try:
                y_points = safe_eval(function_text, x_points)
                y_points = np.array(y_points, dtype = float)

                if y_points.ndim == 0:
                    y_points = np.array([y_points])
            except Exception as e:
                plot_placeholder.error(f"Error evaluating function: {e}")

        if len(x_points) == len(y_points):
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
            height=450,
            xaxis=dict(title="x", range=[a, b]),
            yaxis=dict(title="f(x)", range=[y_min, y_max]),
            showlegend=False,
        )


        # render plotly chart
        plot_placeholder.plotly_chart(fig, use_container_width=False)

    st.divider()


if __name__ == "__main__":
    main()

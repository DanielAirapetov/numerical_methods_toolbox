import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sympy as sp
import os, sys


# need to include this so that importing files works
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)


# each member's functions are stored in a python 
# here I import them to use them later
from sections.optimization.members import daniel, jhon, mark, francis


# function parses through an expression and evaluates symbols in the expression such as trig functions or log(x)
def safe_eval(func: str, x):
    allowed = {
        "x": x,
        "np": np,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "csc": lambda v: 1 / np.sin(v),
        "sec": lambda v: 1 / np.cos(v),
        "cot": lambda v: 1 / np.tan(v),
        "exp": np.exp,
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs,
        "pi": np.pi,
        "e": np.e
    }
    return eval(func, {"__builtins__": {}}, allowed)


# converts text input into a float, if possible
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


    # sets page to wide
    st.set_page_config(layout="wide")

    st.set_page_config(page_title = "Non-linear Optimization")
    st.set_page_config(initial_sidebar_state = "collapsed")


    # remove padding from top of page
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True
                )




    # checks if these keys, which are used in the compute section, already exist
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


    # this is essentially the streamlit version of a horizontal line in html
    st.divider()


    # create columns for the layout of the page heading
    left, center, right = st.columns([1, 3, 1])

    # on the left side of the page we have the back button
    # I added some html and styling using streamlit's markdown attribute which allows for the same use of html and css 
    with left:
        with st.container():
            st.markdown("<div style = 'margin-top: -20px; margin-bottom:50px;'>", unsafe_allow_html = True)
            if st.button("Back"):
                st.switch_page("app.py")
            st.markdown("</div>", unsafe_allow_html = True)
            

    # in the center of the heading there is the title 
    # I used css to center the text and align it with the back button
    with center:
        # set the title with some html for centering and margins
        st.markdown("<h1 style='text-align:center; margin-bottom:-50px; margin-top:3px'>Non-linear Optimization</h1>",unsafe_allow_html=True)



    # this creates a horizontal line and removes the padding from it
    st.markdown("""
        <hr class="custom-line">
        <style>
        .custom-line {
            margin-top: 2rem !important;
            margin-bottom: 0rem !important;
        }
        </style>
        """, unsafe_allow_html=True)


    # add blank space on left and right
    # center the plots and input
    left, center_left, center_right, right = st.columns([0.8, 5, 4, 1])


    # right side of page
    # inputs and selections
    with center_right:

        # I put a div right here simply so I can manually add some padding
        st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

        # st.write displays the text on the screen
        # the hashes are used for changing the size of the text
        # here I didn't need to use any styling so I just used st.write
        st.write("## Enter a Function")


        # this creates a text input and allows the user to enter a function as an expression
        function_text = st.text_input("f(x) =", value="")

        # this checks if the user entered anything for the function
        if function_text.strip():

            # often times ^ is used to signify raising a number to an exponent, so I take care of this by just replacing it with the correct python syntax
            function_text = function_text.replace("^", "**")

            # this part creates a symbolic expression from the string function_text using the sympy library
            try:

                function_symbolic = sp.sympify(function_text, locals = {
                    "sin": sp.sin,
                    "cos": sp.cos,
                    "tan": sp.tan,
                    "log": sp.log,
                    "exp": sp.exp,
                    "sqrt": sp.sqrt,
                    "pi": sp.pi,
                    "e": sp.E
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




        # a column for the method selection, member selection, and delta input all in one row by using streamlit columns
        method_col, member_col, delta_col = st.columns([0.9, 0.9, 1])

        # drop down menu for choosing the method
        with method_col:
            method = st.selectbox(
                "Choose a method",
                options = ["Golden Section", "Newton Min/Max"]
                )

        # drop down menu for choosing the member
        with member_col:
            member = st.selectbox(
                    "Choose a member",
                    options = ["Daniel", "Jhon", "Mark", "Francis"]
                    )

        # input box for entering the delta
        with delta_col:
            delta = float_input("Error threshold", "", key= "delta_key")
            invalid_delta = False

            # delta must be greater than 0
            if delta != None and delta <= 0:
                invalid_delta = True
                st.error("Error threshold must be greater than 0")



        
        # the page looks different depending on the method
        # golden section has bounds while newton method has one initial guess 
        if method == "Golden Section":

            # promt user to enter two bounds which bracket an extrema
            st.markdown("<p style='margin-bottom:-10px;'>Choose bounds that bracket a min/max</p>", unsafe_allow_html=True)

            # here I make two columns side by side for inputing the bounds
            input_box1, input_box2 = st.columns(2)


            # reset these to false whenever the user enters bounds
            invalid_bound_a = False
            invalid_bound_b = False

            # two input boxes
            # under the condition that the function contains log(x) the user shouldn't choose a bound that's <= 0 since those values are out of the domain of log(x)
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


            # create columns for the min/max selection buttons
            min_col, mid_space, max_col = st.columns([1, 0.001, 1])

            if "minmax" not in st.session_state:
                    st.session_state["minmax"] = "Minimum"


            # min button and max button
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

            
            min_max = st.session_state["minmax"]

            # flag is a variable used in each member's golden section method which signifies whether they want to find a min or max
            flag = 1 if min_max == "Minimum" else 2


        else:

            # this section creates the layout of the page when the user choose Newton Min/Max method

            st.markdown("<br>", unsafe_allow_html = True)
            invalid_bound_a = False
            invalid_bound_b = False



            # i reuse the same variable as in Golden Section
            # this line allows the user to enter an initial guess
            left_bound = float_input("Initial Guess: ", "", key = "left_bound_key")

            # this input cannot be <= 0 if the function contains log(x) in it
            if contains_log and left_bound != None:
                if left_bound <= 0:
                    invalid_bound_a = True
                    invalid_bound_b = True
                    st.error("log(x) not defined for x <= 0")





        # section creates a button that computes the result when pressed and displays the result in the column beside it
        compute_button, mid_space2, computed_result = st.columns([1, 0.001, 1])
        

        with compute_button:

            
            # compute button is disabled when there is an invalid input
            disable_compute =  invalid_bound_a or invalid_bound_b or invalid_delta

            # compute button
            if st.button("Compute", disabled = disable_compute, use_container_width = True):

                # the next two if statements check if all input boxes are full
                if function_symbolic != None and function_symbolic != 0 and delta != None:

                    if method == "Golden Section" and left_bound != None and right_bound != None:

                        st.session_state["compute_goldenSection"] = True
                        st.session_state["compute_newtonMinMax"] = False
                        
                        # I used session state to save all the inputs
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




        # here the results are computed based on the user's inputs and the results are then displayed
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


        # this creates temporary values for x and y points in order to display an empty graph when the user hasn't yet entered a function
        x_points = np.linspace(-10, 10, 500)
        y_points = np.full_like(x_points, np.nan)

        data = pd.DataFrame({"x": x_points, "f(x)": y_points})

        plot_placeholder = st.empty()


        # creates columns to put the input boxes for a left and right interval of the graph
        left_space, left_interval, right_interval, right_space = st.columns([0.01, 2, 2, 1])

        # left interval input box with default value -5
        with left_interval:
            a = float_input("Left Bound", -5.00, key = "left_interval_key")
            if contains_log and a != None:
                if a <= 0:
                    st.error("log(x) not defined for x <= 0. Change bound to plot function.")

        # right interval input box with default value 5
        with right_interval:
            b = float_input("Right Bound", 5.00, key = "right_interval_key")
            if contains_log and b != None:
                if b <= 0:
                    st.error("log(x) not defined for x <= 0. Change bound to plot function.")


        # recompute the plot using bounds entered by user
        if a != None and b != None:
            x_points = np.linspace(a, b, 500)
            y_points = np.full_like(x_points, np.nan)

        # if the user entered a function then plot the function
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

        
        if not np.isnan(y_points).all():
            y_min = np.nanmin(y_points)
            y_max = np.nanmax(y_points)
        else:
            y_min, y_max = -10, 10

        # create a plotly figure
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_points, y=y_points, mode="lines", name="f(x)"))

        fig.update_layout(
            width=600,
            height=450,
            xaxis=dict(title="x", range=[a, b]),
            yaxis=dict(title="f(x)", range=[y_min, y_max]),
            showlegend=False,
        )


        # render the plotly chart
        plot_placeholder.plotly_chart(fig, use_container_width=False)


    
    # some styling for aesthetic purposes
    st.markdown("<br><div style = 'margin-top: 35px;'>", unsafe_allow_html = True)
    st.divider()
    st.markdown("</div>", unsafe_allow_html = True)

if __name__ == "__main__":
    main()

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt



st.set_page_config(layout="wide")

# title
st.markdown("<h1 style='text-align:center; margin-bottom:10px; margin-top:-30px'>Optimization Methods</h1>",unsafe_allow_html=True)

# safe evaluation
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


# center the layout
# add blank space on left and right
# center the plots and input
left, center_left, center_right, right = st.columns([1, 4, 4, 1])


# right side of page
# inputs and selections
with center_right:

    st.write("## Enter a Function")
    function_text = st.text_input("f(x) =", value="")

    method = st.selectbox(
            "Choose a Method",
            options = ["Golden Section", "Newton Min/Max"]
            )


    if method == "Golden Section":
        st.markdown("<p style='margin-bottom:-10px;'>Choose bounds that bracket a min/max</p>", unsafe_allow_html=True)
        input_box1, input_box2 = st.columns(2)
        with input_box1:
            left_bound = st.text_input("a: ", value="")
        with input_box2:
            right_bound = st.text_input("b: ", value="")

        min_max = st.segmented_control(
                "",
                options = ["Minimum", "Maximum"],
                default = "Minimum"
                )
        

    elif method == "Newton Min/Max":
        left_bound = st.text_input("Initial Guess", value="")

# plot section with slider to change bounds
with center_left:

    # --- Plot first ---
    x_points = np.linspace(-10, 10, 500)   # temporary defaults (will be overwritten)
    y_points = np.full_like(x_points, np.nan)

    # Empty initial DataFrame
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

    # Recompute plot with user bounds
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
            y=alt.Y(
                "f(x)",
                title="f(x)",
                scale=alt.Scale(
                    domain=[np.nanmin(y_points), np.nanmax(y_points)]
                    if not np.isnan(y_points).all()
                    else [-10, 10]
                )
            )
        )
        .properties(width=600, height=600)
    )

    # Render chart INTO the placeholder ABOVE the input boxes
    plot_placeholder.altair_chart(chart, use_container_width=False)
     
        
        


# ---- Golden Section Method ----
def goldenSectionMethod(a, b, delta, flag, f):

    phi = (1 + np.sqrt(5)) / 2
    error = float('inf')
    iterations = 0
    max_iter = 1000

    x1 = b - ((b - a) / phi)
    x2 = a + ((b - a) / phi)

    while error > delta and iterations < max_iter:

        if flag == 1:
            if f.subs(x, x1) >= f.subs(x, x2):
                a = x1
                x1 = x2
                x2 = a + ((b - a) / phi)
            else:
                b = x2
                x2 = x1
                x1 = b - ((b - a) / phi)

        elif flag == 2:
            if f.subs(x, x1) <= f.subs(x, x2):
                a = x1
                x1 = x2
                x2 = a + ((b - a) / phi)
            else:
                b = x2
                x2 = x1
                x1 = b - ((b - a) / phi)

        error = np.abs(b - a)
        iterations += 1

    return ((a + b) / 2), iterations

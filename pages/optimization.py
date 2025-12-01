import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

from numerical_methods_toolbox/sections/

st.set_page_config(layout="wide")

# ---- Title ----
st.markdown("<h1 style='text-align: center;'>Golden Section Method</h1>", 
            unsafe_allow_html=True)


# ---- Safe evaluation ----
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


# ---- Centered layout: empty - plot - inputs - empty ----
left_spacer, left_col, right_col, right_spacer = st.columns([1, 4, 4, 1])


# RIGHT: Function input
with right_col:
    st.write("## Enter a function f(x):")
    func_text = st.text_input("f(x) =", value="x**2 + 3*x + 2")

    st.write("## Bounds")
    col_a, col_b = st.columns(2)

    with col_a:
        param1 = st.text_input("Left Bound: ", value="")

    with col_b:
        param2 = st.text_input("Right Bound: ", value="")



# LEFT: Plot + slider
with left_col:

    # --- create placeholder for the plot ---
    plot_placeholder = st.empty()

    # --- compute a,b FIRST, but slider appears below ---
    slider_left, slider_center, slider_right = st.columns([1, 5, 1.25])
    with slider_center:
        a, b = st.slider(
            "Interval [a, b]:",
            min_value=-1000.0,
            max_value=1000.0,
            value=(-5.0, 5.0),
            step=0.1
        )

    # --- now draw the plot ABOVE using updated a,b ---
    with plot_placeholder:
        if func_text.strip() != "":
            try:
                xs = np.linspace(a, b, 300)
                ys = safe_eval(func_text, xs)

                df = pd.DataFrame({"x": xs, "f(x)": ys})

                chart = (
                    alt.Chart(df)
                    .mark_line()
                    .encode(x="x", y="f(x)")
                    .properties(width=600, height=600)
                )

                st.altair_chart(chart, use_container_width=False)

            except Exception as e:
                st.error(f"Error evaluating function: {e}")
        else:
            st.info("Enter a valid function.")





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

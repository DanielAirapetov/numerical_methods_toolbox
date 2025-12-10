import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Add project ROOT so imports work
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# ---- Differentiation ----
from sections.calculus.differentiation.danielD import numerical_differentiation
from sections.calculus.differentiation.frankyD import num_diff
from sections.calculus.differentiation.markD import differentiate
from sections.calculus.differentiation.jhonD import numerical_differentation

diff_funcs = {
    "Daniel": numerical_differentiation,
    "Francis": num_diff,
    "Jhon": numerical_differentation,
    "Mark": differentiate
}

# ---- Simpson Integration ----
from sections.calculus.integration.simpson.danielS import simpsonsRule_integration
from sections.calculus.integration.simpson.frankyS import simpsons_rule
from sections.calculus.integration.simpson.markS import simpsonOneThirdMethod
from sections.calculus.integration.simpson.jhonS import simpson_rule

simpson_funcs = {
    "Daniel": simpsonsRule_integration,
    "Francis": simpsons_rule,
    "Jhon": simpson_rule,
    "Mark": simpsonOneThirdMethod
}

# ---- Trapezoid Integration ----
from sections.calculus.integration.trapezoid.danielT import trapezoidRule_integration
from sections.calculus.integration.trapezoid.frankyT import trapezoidal_rule
from sections.calculus.integration.trapezoid.markT import newtonCotesTrapezoidalRuleMethod
from sections.calculus.integration.trapezoid.jhonT import trapezoidal_rule

trapezoid_funcs = {
    "Daniel": trapezoidRule_integration,
    "Francis": trapezoidal_rule,
    "Jhon": trapezoidal_rule,
    "Mark": newtonCotesTrapezoidalRuleMethod
}

def createTable(operation, flag):
    # --- Determine minimum rows ---
    if "min_rows" not in st.session_state:
        if operation == "Trapezoid" or flag == "2-point forward difference":
            st.session_state.min_rows = 2
        else:
            st.session_state.min_rows = 3

    # --- Initialize persistent table once ---
    if "table_data" not in st.session_state:
        st.session_state.table_data = pd.DataFrame({
            "x": [0.0] * st.session_state.min_rows,
            "f(x)": [0.0] * st.session_state.min_rows
        })

    st.subheader("Input Table")
    st.caption("Enter x and f(x) values, then click **Save Table**. Data will persist across reruns.")

    # ---------- EDITOR IN A FORM (no inline “+”) ----------
    with st.form("table_form", clear_on_submit=False):
        edited_df = st.data_editor(
            st.session_state.table_data,
            key="data_editor_widget",
            hide_index=True,
            use_container_width=True,
            num_rows="fixed",     # 🔒 disables inline “+” / “−” inside editor
            column_config={
                "x": st.column_config.NumberColumn("x", step=0.1, format="%.3f"),
                "f(x)": st.column_config.NumberColumn("f(x)", step=0.1, format="%.3f"),
            }
        )
        submitted = st.form_submit_button("Save Table")

    # Commit on Save
    if submitted:
        edited_df = edited_df.copy()
        edited_df["x"] = pd.to_numeric(edited_df["x"], errors="coerce").fillna(0.0)
        edited_df["f(x)"] = pd.to_numeric(edited_df["f(x)"], errors="coerce").fillna(0.0)
        st.session_state.table_data = edited_df.reset_index(drop=True)
        st.rerun()

    # ---------- Row operation buttons ----------
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("Add Row", use_container_width=True):
            st.session_state.table_data = pd.concat(
                [st.session_state.table_data, pd.DataFrame({"x": [0.0], "f(x)": [0.0]})],
                ignore_index=True
            )
            st.rerun()
    with c2:
        if st.button("Remove Row", use_container_width=True):
            if len(st.session_state.table_data) > st.session_state.min_rows:
                st.session_state.table_data = st.session_state.table_data.iloc[:-1].reset_index(drop=True)
                st.rerun()
            else:
                st.warning(f"Minimum {st.session_state.min_rows} rows required.")
    with c3:
        if st.button("Reset Table", use_container_width=True):
            st.session_state.table_data = pd.DataFrame({
                "x": [0.0] * st.session_state.min_rows,
                "f(x)": [0.0] * st.session_state.min_rows
            })
            st.rerun()

    return st.session_state.table_data

def getTable(input_type, flag, operation_type = None):
    if input_type == "GUI":
        df = createTable(operation_type, flag)
    elif input_type == "CSV":
        uploaded = st.file_uploader("Upload CSV", type="csv")
        if uploaded is None:
            st.info("Please upload a CSV file to continue.")
            return None, None
        df = pd.read_csv(uploaded, header=None)
        df.columns = ["x", "f(x)"]

    # Return lists of floats
    x_values = df["x"].astype(float).tolist()
    y_values = df["f(x)"].astype(float).tolist()

    sorted_idx = np.argsort(x_values)
    x_values = np.array(x_values)[sorted_idx].tolist()
    y_values = np.array(y_values)[sorted_idx].tolist()

    return x_values, y_values

def selectMember():
    return st.selectbox("Select whose method to use:", ["Daniel", "Francis", "Jhon", "Mark"])

st.title("Calculus Calculator")
operation = st.selectbox("Choose an operation:", ["Differentiation", "Integration"])
result = None

if operation == "Differentiation":
    # gather inputs: (x_value, x_points, y_points, h, flag, degree)
    flag_label = st.selectbox(
        "Choose the differentiation type:",
        ["2-point forward difference", "3-points forward difference", "3-point centered difference"]
    )
    # Map user-friendly labels to internal flags
    flag_map = {
        "2-point forward difference": "a",
        "3-points forward difference": "b",
        "3-point centered difference": "c"
    }
    flag = flag_map[flag_label]
    input_type = st.selectbox("Choose a input type: ", ["GUI", "CSV"])
    x_points, y_points = getTable(input_type, flag)
    if not x_points or not y_points:
        st.warning("Please enter or upload data points before running this calculation.")
        st.stop()
    x_value = st.number_input("Enter the x value to evaluate the derivative at: ", step=1.0)
    h = st.number_input("Enter the step size:", value=0.1, step=0.1)
    degree = int(st.selectbox("Choose an interpolation degree: ", [2, 3]))
    member = selectMember()

    # call the function
    diff_func = diff_funcs[member]
    result = diff_func(x_value, x_points, y_points, h, flag, degree)
    
elif operation == "Integration":
    flag = None
    method = st.selectbox("Choose a method:", ["Simpson", "Trapezoid"])
    if method == "Simpson":
        input_type = st.selectbox("Choose a input type: ", ["GUI", "CSV"])
        x_points, y_points = getTable(input_type, flag, method)
        if not x_points or not y_points:
            st.warning("Please enter or upload data points before running this calculation.")
            st.stop()
        h = st.number_input("Enter the step size:", value=0.1, step=0.1)
        member = selectMember()

        # call the function
        simpson_func = simpson_funcs[member]
        result = simpson_func(x_points, y_points, h)

    elif method == "Trapezoid":
        input_type = st.selectbox("Choose a input type: ", ["GUI", "CSV"])
        x_points, y_points = getTable(input_type, flag, method)
        if not x_points or not y_points:
            st.warning("Please enter or upload data points before running this calculation.")
            st.stop()
        h = st.number_input("Enter the step size:", value=0.1, step=0.1)
        member = selectMember()

        # call the function
        trap_func = trapezoid_funcs[member]
        result = trap_func(x_points, y_points, h)

if result is not None:
    st.subheader("Result")
    st.write("**Computed Value:**", result)

    # 1) Reserve a spot ABOVE the controls for the graph
    graph_ph = st.empty()

    # 2) Controls BELOW the graph
    st.subheader("Graph Window Settings")
    default_xmin, default_xmax = float(min(x_points)), float(max(x_points))
    default_ymin, default_ymax = float(min(y_points)), float(max(y_points))
    y_range = default_ymax - default_ymin if default_ymax != default_ymin else 1
    default_ymin -= 0.1 * y_range
    default_ymax += 0.1 * y_range

    # Create 2 columns, left for x, right for y
    col_left, col_right = st.columns(2)

    with col_left:
        x_min = st.number_input("X-axis minimum", value=default_xmin, step=1.0, key="x_min_num")
        x_max = st.number_input("X-axis maximum", value=default_xmax, step=1.0, key="x_max_num")

    with col_right:
        y_min = st.number_input("Y-axis minimum", value=default_ymin, step=1.0, key="y_min_num")
        y_max = st.number_input("Y-axis maximum", value=default_ymax, step=1.0, key="y_max_num")

    # (Optional) basic guard so bad limits don't crash the plot
    if x_min >= x_max: x_min, x_max = default_xmin, default_xmax
    if y_min >= y_max: y_min, y_max = default_ymin, default_ymax

    # 3) Build the figure AFTER reading controls, then render into the placeholder
    fig, ax = plt.subplots()

    # Scatter the original data points
    ax.scatter(x_points, y_points, label="Data Points")

    # ----- DIFFERENTIATION -----
    if operation == "Differentiation":
        # Smooth function curve
        x_dense = np.linspace(min(x_points), max(x_points), 800)
        y_dense = np.interp(x_dense, x_points, y_points)
        ax.plot(x_dense, y_dense, color="#007ACC", linewidth=2, alpha=0.9, label="Function Curve")

        # Tangent line (localized for clarity)
        f_x = np.interp(x_value, x_points, y_points)
        slope = result

        # Limit tangent line to a small region around x_value
        x_range = x_max - x_min
        x_line = np.linspace(x_value - 0.25 * x_range, x_value + 0.25 * x_range, 200)
        y_line = f_x + slope * (x_line - x_value)

        ax.plot(
            x_line, y_line,
            color="#FF7F0E",
            linestyle="--",
            linewidth=1.8,
            alpha=0.9,
            label="Tangent Line"
        )

        # Tangent point
        ax.scatter([x_value], [f_x], color="#D62728", s=70, label="Tangent Point")

        # Slope label
        ax.annotate(f"slope ≈ {slope:.4g}", xy=(x_value, f_x),
                    xytext=(10, 10), textcoords="offset points", fontsize=9)

        # Optional: coordinate label for the tangent point
        ax.annotate(f"({x_value:.2f}, {f_x:.2f})",
                    xy=(x_value, f_x),
                    xytext=(10, -15),
                    textcoords="offset points",
                    fontsize=9,
                    color="#D62728")

        # Styling
        ax.set_title("Derivative Visualization", fontsize=13, weight="bold")
        ax.grid(True, linestyle="--", alpha=0.6)

    # ----- INTEGRATION -----
    elif operation == "Integration":
        # Smooth function curve for cleaner visualization
        x_dense = np.linspace(min(x_points), max(x_points), 800)
        y_dense = np.interp(x_dense, x_points, y_points)

        # Function curve
        ax.plot(
            x_dense, y_dense,
            color="#007ACC",
            linewidth=2,
            alpha=0.9,
            label="Function Curve"
        )

        # Shaded integrated area
        ax.fill_between(
            x_dense, y_dense,
            color="#A7C7E7",
            alpha=0.45,
            label="Integrated Area"
        )

        # Optional visual cue for boundaries
        ax.scatter(
            [x_points[0], x_points[-1]],
            [y_points[0], y_points[-1]],
            color="#D62728",
            s=50,
            label="Integration Bounds"
        )

        # Gridlines and labels
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_title("Integral Visualization", fontsize=13, weight="bold")

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    fig.tight_layout()

    # Render once, above the controls
    graph_ph.pyplot(fig)
import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Back Button 
col_back, _ = st.columns([1, 5])
with col_back:
    if st.button("Back"):
        st.switch_page("app.py")

# Add project ROOT so imports work
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

# Differentiation
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

# Simpson Integration
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

# Trapezoid Integration
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
    # Determine minimum rows based on operation/flag
    if operation == "Trapezoid" or flag == "a":   # "a" == 2-point forward
        min_rows = 2
    else:
        min_rows = 3

    # Initialize row count in session state
    if "table_rows" not in st.session_state:
        st.session_state.table_rows = min_rows

    # Enforce minimum in case operation/flag changes
    if st.session_state.table_rows < min_rows:
        st.session_state.table_rows = min_rows

    rows = st.session_state.table_rows

    st.subheader("Input Table")

    # Base DF is only used for shape; values are overridden by widget state
    default_df = pd.DataFrame(
        {
            "x": [0.0] * rows,
            "f(x)": [0.0] * rows
        }
    )

    edited_df = st.data_editor(
        default_df,
        key="table_editor",
        hide_index=True,
        use_container_width=True,
        column_config={
            "x": st.column_config.NumberColumn("x", step=1e-6, format="%.6f"),
            "f(x)": st.column_config.NumberColumn("f(x)", step=1e-6, format="%.6f"),
        }
    )

    # Row control BELOW the table
    col1, _ = st.columns(2)
    with col1:
        new_rows = st.number_input(
            "Number of points",
            min_value=min_rows,
            max_value=50,
            value=rows,
            step=1,
            key="rows_input"
        )

    # If user changes row count → update and rebuild table
    if new_rows != rows:
        st.session_state.table_rows = new_rows
        st.rerun()

    # Return what the user sees in the editor
    return edited_df

def getTable(input_type, flag, operation_type=None):
    if input_type == "GUI":
        df = createTable(operation_type, flag)

        # Clean up the values coming from the editor
        df = df.copy()
        df["x"] = pd.to_numeric(df["x"], errors="coerce").fillna(0.0)
        df["f(x)"] = pd.to_numeric(df["f(x)"], errors="coerce").fillna(0.0)

    elif input_type == "CSV":
        uploaded = st.file_uploader("Upload CSV", type="csv")
        if uploaded is None:
            st.info("Please upload a CSV file to continue.")
            return None, None
        df = pd.read_csv(uploaded, header=None)
        df.columns = ["x", "f(x)"]
        df["x"] = pd.to_numeric(df["x"], errors="coerce").fillna(0.0)
        df["f(x)"] = pd.to_numeric(df["f(x)"], errors="coerce").fillna(0.0)

    # Return lists of floats
    x_values = df["x"].astype(float).tolist()
    y_values = df["f(x)"].astype(float).tolist()

    return x_values, y_values

def _build_uniform_simpson_grid(x_points, y_points, h_input):
    a, b = x_points[0], x_points[-1]

    # Start from user's h, convert to an even number of subintervals
    n = max(2, int(round((b - a) / float(h_input))))
    if n % 2 == 1:  # must be even
        n += 1

    h_eff = (b - a) / n
    Xu = [a + k * h_eff for k in range(n + 1)]
    Yu = np.interp(Xu, x_points, y_points).tolist()
    return Xu, Yu, h_eff, n

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
        st.stop()

    x_sorted = np.array(x_points, dtype=float)
    y_sorted = np.array(y_points, dtype=float)
    sort_idx = np.argsort(x_sorted)
    x_sorted = x_sorted[sort_idx]
    y_sorted = y_sorted[sort_idx]

    x_value = st.number_input("Enter the x value to evaluate the derivative at:", step=1.0, format="%.6f")
    h = st.number_input("Enter the step size:", value=0.01, step=0.01, format="%.6f")
    degree = int(st.selectbox("Choose an interpolation degree: ", [2, 3]))
    member = selectMember()

    # Input validation
    problems = []
    # 1. Detect placeholder (default zero) table first
    if all(v == 0 for v in x_points + y_points):
        problems.append("Please replace the default all-zero table with real data points.")
    # 2. Ensure data lists exist
    elif not x_points or not y_points:
        problems.append("Please enter data points before continuing.")
    # 3. Matching lengths
    elif len(x_points) != len(y_points):
        problems.append("The number of x_points and y_points must match.")
    # 4. Enough points for interpolation degree
    elif len(x_points) <= degree:
        problems.append(f"You need at least {degree + 1} data points for degree {degree} interpolation.")
    # 5. No duplicate x-values
    elif len(set(x_points)) != len(x_points):
        problems.append("Duplicate x-values detected, each x must be unique.")
    # 6. Check numeric types
    if any(not isinstance(x, (int, float)) for x in x_points):
        problems.append("All x-values must be numeric.")
    if any(not isinstance(y, (int, float)) for y in y_points):
        problems.append("All f(x) values must be numeric.")
    if not isinstance(x_value, (int, float)):
        problems.append("The x-value must be numeric.")
    if not isinstance(h, (int, float)) or h == 0:
        problems.append("Step size must be a non-zero number.")
    # 7. Display warnings if needed
    if problems:
        st.warning(problems[0])
        st.stop()

    # call the function
    diff_func = diff_funcs[member]
    if member == "Daniel":
        result = diff_func(x_value, x_sorted, y_sorted, h, flag, degree)
    elif member == "Francis":
        result = diff_func(x_value, x_sorted, y_sorted, h, flag, 1 if degree == 2 else 2)
    elif member == "Jhon":
        result = diff_func(x_value, np.array(x_sorted), np.array(y_sorted), h, flag, degree - 1)
    elif member == "Mark":
        result = diff_func(x_value, np.array(x_sorted), np.array(y_sorted), h, flag, degree + 1)
    
elif operation == "Integration":
    flag = None
    method = st.selectbox("Choose a method:", ["Simpson", "Trapezoid"])
    if method == "Simpson":
        input_type = st.selectbox("Choose a input type: ", ["GUI", "CSV"])
        x_points, y_points = getTable(input_type, flag, method)
        if not x_points or not y_points:
            st.stop()

        x_sorted = np.array(x_points, dtype=float)
        y_sorted = np.array(y_points, dtype=float)
        sort_idx = np.argsort(x_sorted)
        x_sorted = x_sorted[sort_idx]
        y_sorted = y_sorted[sort_idx]

        h = st.number_input("Enter the step size:", value=0.01, step=0.01, format="%.6f")
        member = selectMember()

        # Input validation
        problems = []
        # 1. Detect placeholder (default zero) table first
        if all(v == 0 for v in x_points + y_points):
            problems.append("Please replace the default all-zero table with real data points.")
        # 2. Ensure data lists exist
        elif not x_points or not y_points:
            problems.append("Please enter data points before continuing.")
        # 3. Matching lengths
        elif len(x_points) != len(y_points):
            problems.append("The number of x_values and y_values must match.")
        # 4. Minimum required points for Simpson’s Rule
        elif len(x_points) < 3:
            problems.append("At least three points are required for Simpson’s rule.")
        # 5. Step size validity
        elif not isinstance(h, (int, float)) or h <= 0:
            problems.append("Step size (h) must be a positive number.")
        # 6. Strictly increasing x-values
        elif any(x_sorted[i] <= x_sorted[i - 1] for i in range(1, len(x_points))):
            problems.append("x_values must be strictly increasing after sorting.")
        # 7. Check numeric types
        if any(not isinstance(x, (int, float)) for x in x_points):
            problems.append("All x-values must be numeric.")
        if any(not isinstance(y, (int, float)) for y in y_points):
            problems.append("All f(x) values must be numeric.")
        # 8. Display warnings if needed
        if problems:
            st.warning(problems[0])
            st.stop()

        # call the function
        simpson_func = simpson_funcs[member]
        if member == "Daniel":
            result = simpson_func(x_sorted, y_sorted, h)
        elif member == "Francis":
            a, b = x_points[0], x_points[-1]
            Xu, Yu, h_eff, n_even = _build_uniform_simpson_grid(x_sorted, y_sorted, h)
            result = simpson_func(Xu, Yu, h_eff)
        elif member == "Jhon":
            # Convert to NumPy arrays for compatibility
            x_np = np.array(x_sorted, dtype=float)
            y_np = np.array(y_sorted, dtype=float)
            # Regrid with equal 0.1 spacing (expected by his logic)
            x_fixed = np.round(np.linspace(x_np.min(), x_np.max(), len(x_np)), 1)
            y_fixed = np.interp(x_fixed, x_np, y_np)
            # Run and scale result (his algorithm assumes smaller units)
            result = simpson_func(x_fixed, y_fixed, 0.1) * 100
        elif member == "Mark":
            x_np = np.array(x_sorted, dtype=float)
            y_np = np.array(y_sorted, dtype=float)

            # Calculate h safely
            h = float((x_np[-1] - x_np[0]) / (len(x_np) - 1))

            # Ensure even number of subintervals
            n = int((x_np[-1] - x_np[0]) / h)
            if n % 2 != 0:
                n -= 1
                h = (x_np[-1] - x_np[0]) / n

            result = simpson_func(x_np, y_np, h)

    elif method == "Trapezoid":
        input_type = st.selectbox("Choose a input type: ", ["GUI", "CSV"])
        x_points, y_points = getTable(input_type, flag, method)
        if not x_points or not y_points:
            st.stop()

        x_sorted = np.array(x_points, dtype=float)
        y_sorted = np.array(y_points, dtype=float)
        sort_idx = np.argsort(x_sorted)
        x_sorted = x_sorted[sort_idx]
        y_sorted = y_sorted[sort_idx]

        h = st.number_input("Enter the step size:", value=0.01, step=0.01, format="%.6f")
        member = selectMember()

        # Input validation
        problems = []
        # 1. Detect placeholder (default zero) table first
        if all(v == 0 for v in x_points + y_points):
            problems.append("Please replace the default all-zero table with real data points.")
        # 2. Ensure data lists exist
        elif not x_points or not y_points:
            problems.append("Please enter data points before continuing.")
        # 3. Matching lengths
        elif len(x_points) != len(y_points):
            problems.append("The number of x_values and y_values must match.")
        # 4. Minimum required points for Trapezoid Rule
        elif len(x_points) < 2:
            problems.append("At least two points are required for integration.")
        # 5. Step size validity
        elif not isinstance(h, (int, float)) or h <= 0:
            problems.append("Step size (h) must be a positive number.")
        # 6. Strictly increasing x-values
        elif any(x_sorted[i] <= x_sorted[i - 1] for i in range(1, len(x_points))):
            problems.append("x_values must be strictly increasing after sorting.")
        # 7. Check numeric types
        if any(not isinstance(x, (int, float)) for x in x_points):
            problems.append("All x-values must be numeric.")
        if any(not isinstance(y, (int, float)) for y in y_points):
            problems.append("All f(x) values must be numeric.")
        # 8. Display warnings if needed
        if problems:
            st.warning(problems[0])
            st.stop()

        # call the function
        trap_func = trapezoid_funcs[member]
        if member == "Daniel":
            result = trap_func(x_sorted, y_sorted, h)
        elif member == "Francis":
            x_np = np.round(np.array(x_sorted, dtype=float), 1)
            y_np = np.round(np.array(y_sorted, dtype=float), 5)
            h = round((x_np[-1] - x_np[0]) / (len(x_np) - 1), 1)
            result = trap_func(x_np, y_np, h)
        elif member == "Jhon":
            x_np = np.array(x_sorted, dtype=float)
            y_np = np.array(y_sorted, dtype=float)
            x_np = np.round(x_np, 3)
            y_np = np.round(y_np, 3)
            h = float(np.round((x_np[-1] - x_np[0]) / (len(x_np) - 1), 3))
            result = trap_func(x_np, y_np, h)
        elif member == "Mark":
            x_np = np.array(x_sorted, dtype=float)
            y_np = np.array(y_sorted, dtype=float)
            h = float((x_np[-1] - x_np[0]) / (len(x_np) - 1))
            if len(x_np) <= 3:
                result = trap_func(x_np, y_np, h)  
            else:
                result = trap_func(x_np, y_np, h)

if result is not None:
    st.subheader("Result")
    st.write("**Computed Value:**", result)

    # 1) Reserve a spot ABOVE the controls for the graph
    graph_ph = st.empty()

    # --- Compute fresh default window correctly ---
    default_xmin, default_xmax = float(min(x_points)), float(max(x_points))
    default_ymin, default_ymax = float(min(y_points)), float(max(y_points))

    y_range = default_ymax - default_ymin if default_ymax != default_ymin else 1.0
    x_range = default_xmax - default_xmin if default_xmax != default_xmin else 1.0

    # Add a small 5% x margin and 10% y margin
    default_xmin -= 0.05 * x_range
    default_xmax += 0.05 * x_range
    default_ymin -= 0.1 * y_range
    default_ymax += 0.1 * y_range

    # --- Floor/Ceil defaults (cleaner numbers) ---
    init_x_min = math.floor(default_xmin)
    init_x_max = math.ceil(default_xmax)
    init_y_min = math.floor(default_ymin)
    init_y_max = math.ceil(default_ymax)

    # --- Reset window when data changes ---
    axes_sig = (
        operation,
        len(x_points),
        float(min(x_points)), float(max(x_points)),
        len(y_points),
        float(min(y_points)), float(max(y_points))
    )
    if "axes_sig" not in st.session_state or st.session_state.axes_sig != axes_sig:
        st.session_state.axes_sig = axes_sig
        st.session_state.x_min_num = init_x_min
        st.session_state.x_max_num = init_x_max
        st.session_state.y_min_num = init_y_min
        st.session_state.y_max_num = init_y_max

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

    # Differentiation
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

    # Integration
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
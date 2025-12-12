import streamlit as st
import os, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)







def main():

    st.set_page_config(layout = "wide")

    
    # remove padding from top of page
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True
                )

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
        st.markdown("<h1 style='text-align:center; margin-bottom:-20px; margin-top:-5px'>Documentation</h1>",unsafe_allow_html=True)


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

    # non-linear equations documentation
    st.markdown("<br><br><h2 style = 'text-align:center'>Non-linear Equations</h2>", unsafe_allow_html = True)

    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'>To enter an equation, use ** for powers, * for multiplication, / for division, + for addition, and - for subtraction. Use parentheses for order of precedence and to keep everything organized. You can write functions like sin(x), cos(x), tan(x), sqrt(x), exp(x), and many more.</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'>Once you type your equation, a graph of it will automatically appear, so you can easily choose a suitable range or an initial guess. After that, simply select the method you wish to use, specify its implications, set the flag, determine the tolerance, and provide the range or initial guess for the root. Then the program will find the root for you.</p>", unsafe_allow_html = True)


    # linear systems documentation
    st.markdown("<br><br><h2 style = 'text-align:center'>Linear Systems</h2>", unsafe_allow_html = True)


    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'>This page provides tools for solving linear systems using both direct (Gaussian and Gauss–Jordan elimination) and iterative (Jacobi and Gauss–Seidel) methods. Users may enter an augmented matrix either through the built-in GUI editor or by uploading a CSV file, but in all cases the matrix must be n x (n+1).</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'>Direct methods require only that the coefficient matrix be square and nonsingular, while iterative methods require additional conditions for convergence: the coefficient matrix should ideally be strictly diagonally dominant or symmetric positive definite, and poorly conditioned matrices may lead to slow convergence or divergence.</p>", unsafe_allow_html = True)
 
    st.markdown("<br><p style = 'text-align:justify'>The interface allows users to select a method type, input format, and the group member’s implementation to run. After computation, the solution vector (and iteration count when applicable) is displayed directly through Streamlit.</p>", unsafe_allow_html = True)


    # calculus documentation
    st.markdown("<br><br><h2 style = 'text-align:center'>Calculus</h2>", unsafe_allow_html = True)


    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'> The Calculus Tool is used for solving differentiation and integration problems. Users can enter data points and our backend will approximate a function to apply operations on. Users can specify the point for differentiation, the type of differentiation they want, the step size, an interpolation degree, and any member's function. Results will be displayed graphically, and via text.</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'> To use this tool, you can select between differentiation or integration. When selecting a differentiation type, forward requires data points to come after the target point, centered requires data points to surround the target point. Data points can be entered via a GUI or a properly formatted CSV file. For the most accurate results, confirm that the step size is evenly divisible by the difference in data points, lower values are typically better.</p>", unsafe_allow_html = True)

    st.markdown("<br><p style = 'text-align:justify'> To avoid having any issues/errors, be sure to read any warnings displayed in green text at the bottom of the Calculus Page. Note that adding/removing rows via the GUI will reset the point data, so perform these changes before entering in any data. Be aware that more points will result in higher accuracy and smoother function graphs. The integration interval is taken from the min x point to the max x point. All functions are approximated with Lagrangian Interpolation.</p>", unsafe_allow_html = True)
 
 

    # optimization documentation
    st.markdown("<br><br><h2 style = 'text-align:center'>Non-linear Optimization</h2>", unsafe_allow_html = True)



    l, m, r = st.columns([1, 3, 1])
    with m:
        st.markdown("<p style = 'text-align:center'>This tool allows for the evaluation of the minimum or maximum of a function on a particular interval. The tool has functionality for two methods of non-linear optimization: Golden-Section and Newton Min/Max. It returns the value of the point on the x-axis where there is a min/max and the number of iterations the method took to reach a result</p>", unsafe_allow_html = True)

    left, mid, right = st.columns([1, 0.05, 1])
    with left:


        st.markdown("<br><h5 style = 'text-align:justify'>How to Use:</h5><h6 style = 'text-align:center'>Golden-Section:</h6><ul><li>To evaluate the max/min of a function using the Golden-Section method, enter a function and choose a left and right bound which enclose a min/max</li><li>Enter a value for the acceptable error threshold; this number determines the level of accuracy of the result</li><li>Select whether you would like to find a minimum or a maximum and then press compute</li></ul><br><h6 style = 'text-align:center'>Newton Min/Max:</h6><ul><li>To evaluate the min/max of a function using the Newton Min/Max method, enter a function and enter an initial guess for the min/max of the function</li><li>The result of this method is dependent on the initial guess as the result will either be a minimum or a maximum depending on which is closer</li><li>Similar to the Golden-Section method, this method also requires a value for the acceptable error threshold which indicates the level of accuracy of the result</li></ul>", unsafe_allow_html = True)

    with right:
        st.markdown("<br><h5 style = 'text-align: justify'>Extra Tips:</h5><ul><li>The user may enter various functions and even functions containing pi or e^x. The user may also use functions such as log(x), trigonometric functions and inverse trigonometric functions</li><li>When entering some functions such as log(x), consider the domain of the function when selecting points<li>After entering a function, use the graph to analyze the function and locate an interval which brackets a min/max or to make an initial guess for the min/max</li><li>Note: You can use either ^ or ** to represent raising a number to an exponent</li><li>Other operations are represented by *, /, +, -, and parentheses can be used for grouping</li></ul>", unsafe_allow_html = True)

    st.markdown("<br><br>", unsafe_allow_html = True)
    st.divider()

if __name__ == "__main__":
    main()


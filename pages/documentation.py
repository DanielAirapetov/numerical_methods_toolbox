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


    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    st.markdown("<br><p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)




    st.markdown("<br><br><h2 style = 'text-align:center'>Signal Processing</h2>", unsafe_allow_html = True)


    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    st.markdown("<br><p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)


if __name__ == "__main__":
    main()


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



    
    st.markdown("<br><br><h2 style = 'text-align:center'>Non-linear Equations</h2>", unsafe_allow_html = True)


    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)
 
    st.markdown("<br><p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)




    st.markdown("<br><br><h2 style = 'text-align:center'>Linear Systems</h2>", unsafe_allow_html = True)


    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)
 
    st.markdown("<br><p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)



    st.markdown("<br><br><h2 style = 'text-align:center'>Calculus</h2>", unsafe_allow_html = True)


    left, mid, right = st.columns([1, 0.05, 1])

    with left:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    with right:
        st.markdown("<p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)

    st.markdown("<br><p style = 'text-align:justify'> Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>", unsafe_allow_html = True)
 
 


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

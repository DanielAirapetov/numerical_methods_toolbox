import streamlit as st


def main():

    # declaring some config settings for the page
    st.set_page_config(page_title = "Numerical Methods Toolbox")
    st.set_page_config(layout = "wide")
    st.set_page_config(initial_sidebar_state = "collapsed")


    # remove padding from top of page
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
        }
        </style>
        """, unsafe_allow_html = True)

    #st.markdown("<br>", unsafe_allow_html = True)
    #st.markdown("<br>", unsafe_allow_html = True)

    st.divider()

    left, center, right = st.columns([1, 3, 1])


    with center:
        # this writes the title and names of authors with some html for centering and margins
        st.markdown("<h1 style='text-align:center; margin-bottom:-20px;'>Numerical Methods Toolbox</h1>",unsafe_allow_html=True)
        st.markdown("<br><h3 style='text-align:center;'>Daniel Airepetov, Jhon Palaguachi, Mark Pepaj, Francis Scullin</h3>", unsafe_allow_html = True)




    # this creates a horizontal line and removes the padding from it
    st.markdown("""
        <hr class="custom-line">
        <style>
        .custom-line {
            margin-top: 0rem !important;
            margin-bottom: 0rem !important;
        }
        </style>
        """, unsafe_allow_html=True)






    # html link that navigates to documentation page
    st.markdown(
            """
            <div style = 'text-align: center; margin-top:30px; margin-bottom:-10px;'>
                <a href='./documentation' target = "_self" style='font-size:22px; color:inherit; text-decoration:none;'>
                    See Documentation
                </a>
            </div>
            """, unsafe_allow_html=True)


    
    st.markdown("<h4 style='text-align:center; margin-top:20px'>Welcome! Please select a method below:</h4>", unsafe_allow_html = True)

    # link break using html
    st.markdown("<br>", unsafe_allow_html = True)


    # the following lines first define some styling for the streamlit buttons and then create the buttons with functionality for navigating to different pages
    with st.container():

        st.markdown("""
        <style>
        button {
            height: 80px !important;
        }
        </style>
        """, unsafe_allow_html = True)

        left, mid_left, mid, mid_right, right = st.columns([1, 1, 0.05, 1, 1])

        with mid_left:

            if st.button("Non-linear Equations", use_container_width = True):
                st.switch_page("pages/non_linear_equations.py")

            st.markdown("<br>", unsafe_allow_html = True)

            if st.button("Calculus", use_container_width = True):
                st.switch_page("pages/calculus.py")

        with mid_right:
            if st.button("Linear Systems", use_container_width = True):
                st.switch_page("pages/linear_systems.py")

            st.markdown("<br>", unsafe_allow_html = True)

            if st.button("Non-linear Optimization", use_container_width = True):
                st.switch_page("pages/non_linear_optimization.py")


    st.markdown("<br><br>", unsafe_allow_html = True)

    st.divider()

        
if __name__ == "__main__":
    main()

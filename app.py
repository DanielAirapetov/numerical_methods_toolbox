import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(
    page_title = "Numerical Methods Toolbox",
    initial_sidebar_state = "collapsed" 
)

if "page" not in st.session_state:
    st.session_state.page = "Home"

def navigate_to(page_name):
    st.session_state.page = page_name

def home_page():
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 20px !important;
            }
            .title {
                text-align: center !important;
            }
            .subtitle {
                text-align: center !important;
                margin-top: 20px !important;
                margin-bottom: 20px !important;
            }
            .logo {
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 300px;          
                border: 2px solid black; 
                border-radius: 8px;  
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                margin-top: 20px !important;
                margin-bottom: 20px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<h1 class="title">Numerical Methods Toolbox</h1>', unsafe_allow_html=True)
    st.markdown('<h4 class="subtitle">Made by: Daniel, Jhon, Francis, and Mark</h4>', unsafe_allow_html=True)

    Image_logo = Image.open('Logo.png')
    buffered = BytesIO()
    Image_logo.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    st.markdown(f'<img class="logo" src="data:image/png;base64,{img_str}" alt="Logo">', unsafe_allow_html=True)

    st.markdown('<h4 class="subtitle">Hello! How can we assist you today? Please select an option below.</h4>', unsafe_allow_html=True)

    pages = [
        ["Solving Nonlinear Equations",
        "Solving Linear Systems"],
        
        ["Calculus",
        "Nonlinear Optimization"]
    ]

    st.markdown("""
    <style>
    button {
        height: 80px !important;
        white-space: normal !important;
        font-size: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    for row in pages:
        cols = st.columns(2)

        for i, (col, page) in enumerate(zip(cols, row)):
            with col:
                st.button(
                    page,
                    key=f"{page}_{i}",
                    use_container_width=True,
                    on_click=st.session_state.update,
                    kwargs={"page": page}
                )

        st.markdown("<br>", unsafe_allow_html=True)




def page_content(name):
    st.title(name)
    st.write(f"Content specific to {name}.")
    st.button("Back to Home", on_click=lambda: st.session_state.update(page="Home"))

def main():
    if st.session_state.page == "Home":
        home_page()
    else:
        page_content(st.session_state.page)

if __name__ == "__main__":
    main()

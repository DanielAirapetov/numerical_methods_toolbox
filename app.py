import streamlit as st
from PIL import Image
import base64
from io import BytesIO

pages = [
    ["Solving Nonlinear Equations", "Solving Linear Systems", "Calculus"],
    ["Nonlinear Optimization", "Signal Processing", "About"]
]

page_files = [
    ["root_finding.py", "linear_systems.py", "calculus.py"],
    ["optimization.py", "signal_processing.py", "about.py"]
]

st.set_page_config(
    page_title="Numerical Methods Toolbox",
    initial_sidebar_state="collapsed"
)

def home_page():
    st.markdown(
        """
        <style>
        .block-container { padding-top: 20px !important; }
        .title { text-align: center !important; }
        .subtitle { text-align: center !important; margin-top: 20px !important; margin-bottom: 20px !important; }
        .logo {
            display: block; margin-left: auto; margin-right: auto;
            width: 300px; border: 2px solid black; border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-top: 20px !important; margin-bottom: 20px !important;
        }
        button {
            height: 80px !important; font-size: 15px !important; white-space: normal !important;
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

    st.markdown('<h4 class="subtitle">Hello! How can we assist you today? Please select an option below.</h4>',
                unsafe_allow_html=True)
    
    for row_labels, row_files in zip(pages, page_files):
        cols = st.columns(3)
        for col, label, file in zip(cols, row_labels, row_files):
            with col:
                if st.button(label, use_container_width=True):
                    st.switch_page(f"pages/{file}")
        st.markdown("<br>", unsafe_allow_html=True)

def main():
    home_page()

if __name__ == "__main__":
    main()

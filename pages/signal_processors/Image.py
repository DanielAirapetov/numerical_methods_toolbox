import os,sys
import streamlit as st
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

def main():
    st.set_page_config(
    page_title ="Image FFT/WHT",
    initial_sidebar_state ="collapsed" 
)
def main():
    st.title("Image FFT/WHT")
    
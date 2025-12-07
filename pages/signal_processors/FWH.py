import streamlit as st
import os,sys
from sections.signal_processing.fast_WH import frankie_WH, mark_WH
# Add project ROOT so imports work
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)
    
st.set_page_config(
    page_title ="Fast Walsh Hadamard",
    initial_sidebar_state ="collapsed" 
)
def main():
    st.title("Fast Walsh Hadamard Transformer")
    
    
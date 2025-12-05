import streamlit as st
import os,sys


# Add project ROOT so imports work
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)
    

from pages.signal_processors import FFT, FWH

# List of pages
pages = ["Fast Fourier", "Fast Walsh Hadamard"]

# Map page names to their functions (do NOT call them)
page_functions = {
    "Fast Fourier": FFT.main,
    "Fast Walsh Hadamard": FWH.main
}

# Store the current page in session_state
if "page" not in st.session_state:
    st.session_state.page = "Home"


def navigate_to(page_name):
    st.session_state.page = page_name


def signal_processing():
    st.title("Signal Processing Tools")
    cols = st.columns(2)

    for i, page in enumerate(pages):
        with cols[i % 2]:
            st.button(
                page,
                key=page,
                use_container_width=True,
                on_click=navigate_to,
                args=(page,)
            )


def main():
    if st.session_state.page == "Home":
        signal_processing()
    else:
        if st.session_state.page in page_functions:
            # Execute the chosen page function
            page_functions[st.session_state.page]()
        else:
            st.write(f"Page '{st.session_state.page}' not found.")

if __name__ == "__main__":
    main()

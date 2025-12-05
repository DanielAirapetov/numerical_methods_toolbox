import streamlit as st

st.set_page_config(layout = "wide")
if st.button("Back"):
    st.switch_page("app.py")

st.markdown("<h1 style = 'text-align: center;'>Documentation</h1>", unsafe_allow_html = True)

st.markdown("---")



import streamlit as st
st.set_page_config(
    page_title = "About",
    initial_sidebar_state = "collapsed" 
)

if st.button("Back", use_container_width=True):
    st.switch_page("app.py")

import streamlit as st

def require_login():
    if "user_id" not in st.session_state or st.session_state.user_id is None:
        st.switch_page("app.py")

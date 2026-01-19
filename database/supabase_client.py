import streamlit as st
from supabase import create_client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

def restore_session():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    if "email" not in st.session_state:
        st.session_state.email = None

    try:
        session = supabase.auth.get_session()
        if session and session.user:
            st.session_state.user_id = session.user.id
            st.session_state.email = session.user.email
    except:
        pass

    return supabase

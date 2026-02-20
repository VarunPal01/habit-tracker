import streamlit as st
from database.supabase_client import get_supabase

supabase = get_supabase()

if "user_id" not in st.session_state:
    st.session_state.user_id = None

session = supabase.auth.get_session()
if session and session.user:
    st.session_state.user_id = session.user.id
    st.switch_page("pages/Habits.py")

st.markdown("""
<style>
section[data-testid="stSidebar"] {display:none;}
</style>
""", unsafe_allow_html=True)

st.title("🔐 Life Tracker")

tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            st.session_state.user_id = res.user.id
            st.switch_page("pages/Habits.py")
        except:
            st.error("Invalid credentials")


with tab2:
    email = st.text_input("Email", key="r1")
    password = st.text_input("Password", type="password", key="r2")

    if st.button("Create account"):
        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            if res.user:
                st.success("Account created. Please check your email to confirm.")
            else:
                st.error(f"Registration failed: {res}")

        except Exception as e:
            st.error(f"Registration failed: {e}")
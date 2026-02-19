
import streamlit as st
from supabase import create_client

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Life Tracker",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- SUPABASE CONFIG ----------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- SESSION INIT ----------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "email" not in st.session_state:
    st.session_state.email = None

# ---------------- AUTH UI (LOGIN / REGISTER) ----------------
if st.session_state.user_id is None:

    # Hide sidebar completely
    st.markdown(
        "<style>section[data-testid='stSidebar']{display:none;}</style>",
        unsafe_allow_html=True
    )

    st.title("🔥 Life Tracker")
    st.caption("Simple. Personal. Daily.")

    tab_login, tab_register = st.tabs(["🔐 Login", "🆕 Register"])

    # ---------- LOGIN ----------
    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login")

        if login_btn:
            if not email or not password:
                st.error("Please enter email and password")
            else:
                try:
                    res = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    st.session_state.user_id = res.user.id
                    st.session_state.email = res.user.email

                    st.success("Login successful ✅")
                    st.switch_page("pages/Habits.py")

                except Exception:
                    st.error("Invalid email or password")

    # ---------- REGISTER ----------
    with tab_register:
        with st.form("register_form"):
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")
            register_btn = st.form_submit_button("Create Account")

        if register_btn:
            if not email or not password:
                st.error("Please fill all fields")
            else:
                try:
                    supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })
                    st.success("Account created. Please login.")
                except Exception:
                    st.error("Registration failed")

    st.stop()

# ---------------- DASHBOARD (AFTER LOGIN) ----------------
st.title("🏠 Dashboard")
st.caption(f"Logged in as {st.session_state.email}")

# Logout button (mobile friendly)
if st.button("🚪 Logout"):
    supabase.auth.sign_out()
    st.session_state.user_id = None
    st.session_state.email = None
    st.rerun()

st.divider()

# ---------------- NAVIGATION ----------------
st.subheader("📍 Your Tools")

st.page_link("pages/Habits.py", label="🔥 Habit Tracker")
st.page_link("pages/Tasks.py", label="📌 Tasks")
st.page_link("pages/Meals.py", label="🍽️ Meal Tracker")
st.page_link("pages/Budget.py", label="💰 Budget Tracker")
st.page_link("pages/Calendar.py", label="📅 Calendar")
st.page_link("pages/Vision.py", label="🌈 Vision Board")
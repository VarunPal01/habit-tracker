import streamlit as st
#<<<<<<< HEAD
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
#=======
import json
from datetime import datetime
import os

# ---------------- CONFIG ----------------
# app.py
st.set_page_config(
    page_title="Life Tracker",
    layout="centered"
)


FILE = "tasks.json"

# ---------------- HEADER ----------------
today = datetime.now().strftime("%A")
date = datetime.now().strftime("%d %B %Y")

col1, col2 = st.columns([8, 4])

with col1:
    st.title("📌 Life Tracker")
    st.caption("Simple daily task manager")

with col2:
    st.write("")
    st.markdown(f"**{today}**")
    st.caption(date)

st.divider()

# ---------------- LOAD / SAVE ----------------
def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# ---------------- STATE ----------------
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# ---------------- ADD TASK ----------------
with st.form("task_form", clear_on_submit=True):
    task = st.text_input("➕ Add new task", placeholder="Example: Study Python")
    add = st.form_submit_button("Add Task")

    if add:
        if task.strip():
            st.session_state.tasks.append(task.strip())
            save_tasks(st.session_state.tasks)
            st.rerun()
        else:
            st.warning("Task cannot be empty")

# ---------------- STATS ----------------
total_tasks = len(st.session_state.tasks)
completed = 0  # tasks are removed when done
pending = total_tasks

if total_tasks > 0:
    progress = completed / total_tasks if total_tasks else 0
    st.progress(progress)
    st.caption(f"🕒 {pending} pending task(s)")
else:
    st.info("✨ No tasks yet. Add one to get started!")

st.divider()

# ---------------- TASK LIST ----------------
st.subheader("📋 Today's Tasks")
st.caption("Mark task as done to remove it")

if not st.session_state.tasks:
    st.write("👍 You’re free for now. Enjoy your day!")
else:
    for task in st.session_state.tasks.copy():
        col1, col2 = st.columns([8, 2])

        with col1:
            st.markdown(f"**• {task}**")

        with col2:
            done = st.checkbox("Done", key=f"done_{task}")

        if done:
            st.session_state.tasks.remove(task)
            save_tasks(st.session_state.tasks)
            st.rerun()

st.divider()

# ---------------- CLEAR ALL ----------------
if st.button("🗑️ Clear All Tasks"):
    st.session_state.tasks = []
    save_tasks([])
    st.success("All tasks cleared")
    st.rerun()
#>>>>>>> 4eae2f52fcf32fecbcced50f5c4f6d9c231e3061

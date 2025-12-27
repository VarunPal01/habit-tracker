import streamlit as st
import json
import os
from datetime import datetime
import calendar

# ================== CONFIG ==================
st.set_page_config(page_title="Life Tracker", layout="centered")

TASK_FILE = "tasks.json"
VISION_FILE = "vision.json"

# ================== STATE ==================
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "tasks" not in st.session_state:
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            st.session_state.tasks = json.load(f)
    else:
        st.session_state.tasks = []

if "vision" not in st.session_state:
    if os.path.exists(VISION_FILE):
        with open(VISION_FILE, "r") as f:
            st.session_state.vision = json.load(f)
    else:
        st.session_state.vision = ""

# ================== SIDEBAR ==================
st.sidebar.title("🧠 Life Tracker")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "✅ To-Do", "📅 Calendar", "🎯 Vision Board"]
)

st.session_state.page = page

st.sidebar.divider()
st.sidebar.caption("Built for focus & growth")

# ================== HEADER ==================
today = datetime.now().strftime("%A")
date = datetime.now().strftime("%d %B %Y")

col1, col2 = st.columns([6, 2])
with col1:
    st.title("📌 Life Tracker")
with col2:
    st.markdown(f"**{today}**")
    st.markdown(date)

st.divider()

# ================== PAGES ==================
def home_page():
    st.subheader("🏠 Home")
    st.markdown(
        """
        ### Welcome 👋  
        This is your **personal productivity system**.

        **Features**
        - ✅ Daily task manager  
        - 📅 Monthly calendar  
        - 🎯 Vision board  

        _Small steps daily → Big life changes_
        """
    )

def todo_page():
    st.subheader("✅ To-Do List")
    with st.form("task_form", clear_on_submit=True):
        task = st.text_input("➕ Add new task")
        add = st.form_submit_button("Add")
        if add and task.strip():
            st.session_state.tasks.append(task.strip())
            json.dump(st.session_state.tasks, open(TASK_FILE, "w"))
            st.rerun()
            

    st.divider()
    if not st.session_state.tasks:
        st.info("No tasks yet")
    else:
        for i, task in enumerate(st.session_state.tasks.copy()):
            col1, col2 = st.columns([8, 2])
            col1.write(task)
            if col2.checkbox("Done", key=f"task_{i}_{task}"):
                st.session_state.tasks.remove(task)
                json.dump(st.session_state.tasks, open(TASK_FILE, "w"))
                st.rerun()
                st.divider()

def calendar_page():
    st.subheader("📅 Monthly Calendar")

    now = datetime.now()
    year, month = now.year, now.month
    today_date = now.day

    cal = calendar.monthcalendar(year, month)
    month_name = now.strftime("%B %Y")

    st.markdown(f"### {month_name}")

    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    for i in range(7):
        cols[i].markdown(f"**{days[i]}**")

    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            elif day == today_date:
                cols[i].markdown(
                    f"<div style='padding:10px; border-radius:10px; background:#4CAF50; color:white; text-align:center'>{day}</div>",
                    unsafe_allow_html=True
                )
            else:
                cols[i].markdown(
                    f"<div style='padding:10px; border-radius:10px; border:1px solid #ccc; text-align:center'>{day}</div>",
                    unsafe_allow_html=True
                )

def vision_page():
    st.subheader("🎯 Vision Board")

    vision = st.text_area(
        "Write your goals / vision",
        value=st.session_state.vision,
        height=180
    )

    if st.button("💾 Save Vision"):
        st.session_state.vision = vision
        with open(VISION_FILE, "w") as f:
            json.dump(vision, f)
        st.success("Vision saved")

    if st.session_state.vision:
        st.divider()
        st.markdown("### 🌟 Your Vision")
        st.write(st.session_state.vision)

# ================== ROUTER ==================
if page.startswith("🏠"):
    home_page()
elif page.startswith("✅"):
    todo_page()
elif page.startswith("📅"):
    calendar_page()
elif page.startswith("🎯"):
    vision_page()

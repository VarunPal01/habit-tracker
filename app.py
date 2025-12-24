import streamlit as st
import json
from datetime import datetime
import os

st.set_page_config(page_title="Life Tracker", layout="centered")

# ---------- HEADER ----------
today = datetime.now().strftime("%A")
date = datetime.now().strftime("%d %B %Y")

col1, col2 = st.columns([8, 4])

with col1:
    st.title("📌 Life Tracker")

with col2:
    st.write("")  # spacing
    st.write("")
    st.markdown(f"**{today}**")
    st.markdown(date)

st.divider()

FILE = "tasks.json"

# ---------- LOAD TASKS ----------
def load_tasks():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

# ---------- SAVE TASKS ----------
def save_tasks(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f)

# ---------- STATE ----------
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()


# ---------- ADD TASK ----------
with st.form("task_form", clear_on_submit=True):
    task = st.text_input("➕ Add new task")
    add = st.form_submit_button("Add Task")

    if add:
        if task.strip():
            st.session_state.tasks.append(task.strip())
            save_tasks(st.session_state.tasks)
            st.rerun()
        else:
            st.warning("Task cannot be empty")

# ---------- TASK LIST ----------
st.subheader("📋 Today's Tasks")
st.caption("Tick when completed:")

if not st.session_state.tasks:
    st.info("No tasks yet")
else:
    for i, task in enumerate(st.session_state.tasks.copy()):

        col1, col2 = st.columns([8, 2])

        with col1:
            st.markdown(f"**{task}**")

        with col2:
            done = st.checkbox("Done", key=f"done_{i}")

        if done:
            st.session_state.tasks.remove(task)
            save_tasks(st.session_state.tasks)
            st.rerun()


st.divider()

# ---------- CLEAR ALL ----------
if st.button("🗑️ Clear All Tasks"):
    st.session_state.tasks = []
    save_tasks([])
    st.rerun()


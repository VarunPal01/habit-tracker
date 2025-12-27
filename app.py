import streamlit as st
import json
from datetime import datetime
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Life Tracker", layout="centered")

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

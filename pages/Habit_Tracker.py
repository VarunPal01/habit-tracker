import streamlit as st
import json
import os
from datetime import date

FILE = "database/habits.json"
today = date.today().isoformat()

# ---------- LOAD / SAVE ----------
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {"habits": [], "data": {}}

def save_data(data):
    os.makedirs("database", exist_ok=True)  # ✅ auto-create folder
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


if "habit_data" not in st.session_state:
    st.session_state.habit_data = load_data()

data = st.session_state.habit_data

# ---------- UI ----------
st.title("🔥 Habit Tracker")
st.caption("Track your daily habits like Notion")

st.divider()

# ---------- ADD HABIT ----------
new_habit = st.text_input("➕ Add new habit")

if st.button("Add Habit"):
    if new_habit and new_habit not in data["habits"]:
        data["habits"].append(new_habit)
        save_data(data)
        st.rerun()

# ---------- HABIT TABLE ----------
if not data["habits"]:
    st.info("Add your first habit to start tracking")
else:
    st.subheader(f"📅 Today: {today}")

    completed = 0

    for habit in data["habits"]:
        key = f"{today}_{habit}"
        checked = data["data"].get(key, False)

        col1, col2 = st.columns([8, 2])
        with col1:
            st.write(habit)
        with col2:
            value = st.checkbox("", value=checked, key=key)

        data["data"][key] = value
        if value:
            completed += 1

    save_data(data)

    # ---------- PROGRESS ----------
    progress = completed / len(data["habits"])
    st.divider()
    st.subheader("📊 Daily Progress")
    st.progress(progress)
    st.write(f"**{int(progress * 100)}% completed**")

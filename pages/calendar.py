import streamlit as st
from datetime import date

st.set_page_config(page_title="Calendar & Timetable", layout="centered")

st.title("📅 Calendar & ⏰ Time Table")
st.write("Plan your day easily")

st.divider()

# ---------- CALENDAR ----------
selected_date = st.date_input(
    "📆 Select a date",
    value=date.today()
)

st.success(f"Selected date: {selected_date}")

st.divider()

# ---------- TASK INPUT ----------
st.subheader("📝 Enter your tasks (one per line)")

tasks_input = st.text_area(
    "Example:\nStudy Python\nExercise\nRevision\nProject work",
    height=150
)

st.divider()

# ---------- TIME TABLE SUGGESTER ----------
st.subheader("⏰ Suggested Time Table")

if st.button("Generate Time Table"):
    if not tasks_input.strip():
        st.warning("Please enter at least one task")
    else:
        tasks = [t.strip() for t in tasks_input.split("\n") if t.strip()]

        start_hour = 9  # 9 AM
        duration = 1    # 1 hour per task

        for i, task in enumerate(tasks):
            hour = start_hour + i * duration
            st.write(f"🕘 {hour}:00 - {hour+1}:00 → **{task}**")

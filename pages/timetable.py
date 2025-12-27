import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="Time Table Suggester", layout="centered")

st.title("⏰ Time Table Suggester")

st.divider()

# ---------- TIME RANGE ----------
col1, col2 = st.columns(2)

with col1:
    start_time = st.time_input(
        "Start Time",
        value=datetime.strptime("09:00", "%H:%M").time(),
    )

with col2:
    end_time = st.time_input(
        "End Time",
        value=datetime.strptime("18:00", "%H:%M").time(),
    )

st.divider()

# ---------- TASK INPUT ----------
tasks_text = st.text_area(
    "Enter tasks (one per line)",
    height=180,
    placeholder="Study Python\nExercise\nRevision\nProject work",
)

st.divider()

# ---------- GENERATE ----------
if st.button("Generate Time Table"):
    if not tasks_text.strip():
        st.warning("Please enter tasks")
    else:
        tasks = [t.strip() for t in tasks_text.split("\n") if t.strip()]

        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)

        total_minutes = int((end_dt - start_dt).total_seconds() / 60)

        if total_minutes <= 0:
            st.error("End time must be after start time")
        else:
            per_task = total_minutes // len(tasks)

            st.subheader("📋 Suggested Schedule")

            current = start_dt
            for task in tasks:
                next_time = current + timedelta(minutes=per_task)

                st.write(
                    f"🕒 **{current.strftime('%I:%M %p')} – "
                    f"{next_time.strftime('%I:%M %p')}** → {task}"
                )

                current = next_time

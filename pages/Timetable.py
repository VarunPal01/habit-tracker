import streamlit as st
from datetime import datetime, timedelta
from utils.auth_guard import require_login

st.set_page_config(
    page_title="Timetable",
    page_icon="📅",
    layout="centered"
)

require_login()

st.title("📅 Smart Timetable")

wake = st.time_input("Wake up time")
sleep = st.time_input("Sleep time")

subjects_input = st.text_area(
    "Subjects (comma separated)",
    placeholder="Maths, Physics, Coding"
)

if st.button("Generate"):
    if not subjects_input:
        st.error("Enter subjects")
    elif sleep <= wake:
        st.error("Sleep must be after wake time")
    else:
        subjects = [s.strip() for s in subjects_input.split(",")]
        current = datetime.combine(datetime.today(), wake)

        table = []
        for subject in subjects:
            end = current + timedelta(minutes=60)
            table.append({
                "Time": f"{current.strftime('%H:%M')} - {end.strftime('%H:%M')}",
                "Activity": subject
            })
            current = end

        st.table(table)

import streamlit as st
from datetime import datetime, timedelta

# ---------------- MEMORY ----------------
if "data" not in st.session_state:
    st.session_state.data = {
        "purpose": "",
        "class": "",
        "school_hours": "",
        "wake_time": "06:00",
        "sleep_time": "22:00",
        "subjects": ""
    }

# ---------------- HELPERS ----------------
def parse_time(t):
    if isinstance(t, str):
        return datetime.strptime(t, "%H:%M")
    return t

def generate_timetable(wake, sleep, school_hours, subjects):
    timetable = []

    start = parse_time(wake)
    end = parse_time(sleep)

    # Parse school hours if provided
    school_start = school_end = None
    if school_hours:
        try:
            school_times = school_hours.replace(" ", "").split("-")
            school_start = parse_time(school_times[0])
            school_end = parse_time(school_times[1])
        except:
            school_start = school_end = None

    # Wake up
    timetable.append({"Time": start.strftime("%I:%M %p"), "Activity": "Wake up"})
    current = start + timedelta(minutes=30)

    # Subjects logic
    subjects_blocks = subjects.copy()
    study_block = 60
    break_time = 10
    blocks_done = 0

    while current + timedelta(minutes=study_block) <= end:
        # Skip school hours
        if school_start and school_end and current >= school_start and current < school_end:
            timetable.append({
                "Time": f"{school_start.strftime('%I:%M %p')} - {school_end.strftime('%I:%M %p')}",
                "Activity": "School / College"
            })
            current = school_end
            continue

        # Assign subject
        subject = subjects_blocks[blocks_done % len(subjects_blocks)]
        next_time = current + timedelta(minutes=study_block)
        timetable.append({
            "Time": f"{current.strftime('%I:%M %p')} - {next_time.strftime('%I:%M %p')}",
            "Activity": subject
        })
        current = next_time
        blocks_done += 1

        # Break after every 2 blocks
        if blocks_done % 2 == 0 and current + timedelta(minutes=break_time) < end:
            break_end = current + timedelta(minutes=break_time)
            timetable.append({
                "Time": f"{current.strftime('%I:%M %p')} - {break_end.strftime('%I:%M %p')}",
                "Activity": "Break"
            })
            current = break_end

    # Remaining time
    if current < end:
        timetable.append({
            "Time": f"{current.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}",
            "Activity": "Revision / Free Study"
        })

    # Sleep
    timetable.append({"Time": end.strftime("%I:%M %p"), "Activity": "Sleep"})
    return timetable

# ---------------- UI ----------------
st.title("📅 Smart Time Table Maker")

st.subheader("📝 Details")

st.session_state.data["purpose"] = st.selectbox(
    "What is it for?",
    ["", "School study", "Exam preparation", "Daily routine", "All of these"]
)

st.session_state.data["class"] = st.text_input(
    "Your class / grade",
    value=st.session_state.data["class"]
)

st.session_state.data["school_hours"] = st.text_input(
    "School / College hours (if any, e.g., 09:00-15:00)",
    value=st.session_state.data["school_hours"]
)

st.subheader("⏰ Daily Timing")

wake = st.time_input("Wake-up time", parse_time(st.session_state.data["wake_time"]))
sleep = st.time_input("Sleep time", parse_time(st.session_state.data["sleep_time"]))

st.session_state.data["wake_time"] = wake.strftime("%H:%M")
st.session_state.data["sleep_time"] = sleep.strftime("%H:%M")

st.subheader("📚 Subjects (Required)")
subjects_input = st.text_area(
    "Subjects you study (comma separated)",
    value=st.session_state.data["subjects"],
    placeholder="Maths, Physics, Coding"
)
st.session_state.data["subjects"] = subjects_input

# ---------------- GENERATE ----------------
if st.button("📅 Generate Time Table"):
    if not subjects_input:
        st.error("Please enter at least one subject ❌")
    elif sleep <= wake:
        st.error("Sleep time must be after wake-up time ❌")
    else:
        subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]
        timetable = generate_timetable(
            st.session_state.data["wake_time"],
            st.session_state.data["sleep_time"],
            st.session_state.data["school_hours"],
            subjects
        )
        st.success("✅ Smart Daily Time Table Including School Hours")
        st.table(timetable)

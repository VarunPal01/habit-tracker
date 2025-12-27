import streamlit as st
import calendar
import json
import os
from datetime import date

st.set_page_config(page_title="Monthly Calendar", layout="wide")

FILE = "calendar_events.json"
today = date.today()

# ---------- LOAD / SAVE ----------
def load_events():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_events(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

if "events" not in st.session_state:
    st.session_state.events = load_events()

st.title("🗓️ Monthly Calendar")

# ---------- MONTH / YEAR ----------
col1, col2 = st.columns(2)

with col1:
    year = st.selectbox(
        "Year",
        list(range(2023, 2031)),
        index=list(range(2023, 2031)).index(today.year),
    )

with col2:
    month = st.selectbox(
        "Month",
        list(range(1, 13)),
        index=today.month - 1,
        format_func=lambda x: calendar.month_name[x],
    )

st.subheader(f"{calendar.month_name[month]} {year}")

# ---------- CSS FOR GOOGLE STYLE GRID ----------
st.markdown(
    """
    <style>
    .calendar {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        border: 1px solid #ccc;
    }
    .day-header {
        border-right: 1px solid #ccc;
        border-bottom: 1px solid #ccc;
        padding: 8px;
        font-weight: bold;
        text-align: center;
        background: #f7f7f7;
    }
    .cell {
        border-right: 1px solid #ccc;
        border-bottom: 1px solid #ccc;
        min-height: 120px;
        padding: 6px;
        font-size: 14px;
    }
    .today {
        background-color: #fff3f3;
        border: 2px solid #ff4b4b;
    }
    .date-number {
        font-weight: bold;
        margin-bottom: 4px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- DAY HEADERS ----------
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

html = "<div class='calendar'>"
for d in days:
    html += f"<div class='day-header'>{d}</div>"

# ---------- CALENDAR GRID ----------
cal = calendar.monthcalendar(year, month)

for week in cal:
    for day in week:
        if day == 0:
            html += "<div class='cell'></div>"
        else:
            is_today = (
                day == today.day
                and month == today.month
                and year == today.year
            )

            date_key = f"{year}-{month:02d}-{day:02d}"
            events = st.session_state.events.get(date_key, [])

            cell_class = "cell today" if is_today else "cell"

            html += f"<div class='{cell_class}'>"
            html += f"<div class='date-number'>{day}</div>"

            for e in events:
                html += f"<div>• {e}</div>"

            html += "</div>"

html += "</div>"

st.markdown(html, unsafe_allow_html=True)

st.divider()

# ---------- ADD EVENT ----------
st.subheader("➕ Add Event")

col1, col2 = st.columns(2)

with col1:
    event_day = st.number_input(
        "Day",
        min_value=1,
        max_value=31,
        step=1,
        value=today.day,
    )

with col2:
    event_text = st.text_input("Event")

if st.button("Add Event"):
    if event_text.strip():
        key = f"{year}-{month:02d}-{event_day:02d}"
        st.session_state.events.setdefault(key, []).append(event_text)
        save_events(st.session_state.events)
        st.rerun()

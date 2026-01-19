import streamlit as st
import calendar
import json
import os
from datetime import date, datetime
from zoneinfo import ZoneInfo
from database.supabase_client import restore_session
from utils.auth_guard import require_login

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Calendar",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- AUTH ----------------
restore_session()
require_login()

user_id = st.session_state.user_id
today = date.today()
LOCAL_TZ = ZoneInfo("Asia/Kolkata")

# ---------------- STORAGE ----------------
FILE = "calendar_events.json"

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

# ---------------- HEADER ----------------
st.title("📅 Calendar")
st.caption("Monthly Planner")
st.divider()

# ---------------- MONTH / YEAR ----------------
c1, c2 = st.columns(2)

with c1:
    year = st.selectbox(
        "Year",
        list(range(2023, 2031)),
        index=list(range(2023, 2031)).index(today.year),
    )

with c2:
    month = st.selectbox(
        "Month",
        list(range(1, 13)),
        index=today.month - 1,
        format_func=lambda x: calendar.month_name[x],
    )

st.subheader(f"{calendar.month_name[month]} {year}")

# ---------------- WEEK HEADER ----------------
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
cols = st.columns(7)
for i, d in enumerate(days):
    cols[i].markdown(f"**{d}**")

# ---------------- CALENDAR GRID ----------------
cal = calendar.monthcalendar(year, month)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        with cols[i]:
            if day == 0:
                st.write("")
            else:
                date_key = f"{year}-{month:02d}-{day:02d}"
                events = st.session_state.events.get(date_key, [])

                if day == today.day and month == today.month and year == today.year:
                    st.success(f"**{day}**")
                else:
                    st.markdown(f"**{day}**")

                for e in events:
                    st.caption(f"• {e}")

# ---------------- YEAR COUNTDOWN ----------------
st.divider()
st.subheader("⏳ Year Countdown")

now = datetime.now(LOCAL_TZ)
end = datetime(year, 12, 31, 23, 59, 59, tzinfo=LOCAL_TZ)
diff = int((end - now).total_seconds())

if diff > 0:
    d, r = divmod(diff, 86400)
    h, r = divmod(r, 3600)
    m, s = divmod(r, 60)
    st.info(f"{d} days {h:02d}:{m:02d}:{s:02d}")
else:
    st.success("🎉 Happy New Year!")

# ---------------- ADD EVENT ----------------
st.divider()
st.subheader("➕ Add Event")

max_day = calendar.monthrange(year, month)[1]

c1, c2, c3 = st.columns([2, 6, 2])

with c1:
    event_day = st.number_input("Day", 1, max_day, today.day)

with c2:
    event_text = st.text_input("Event")

with c3:
    if st.button("Add"):
        if event_text.strip():
            key = f"{year}-{month:02d}-{event_day:02d}"
            st.session_state.events.setdefault(key, []).append(event_text)
            save_events(st.session_state.events)
            st.success("Event added")
            st.rerun()

import streamlit as st
import calendar
import json
import os
from datetime import date, datetime
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=1000, key="countdown_refresh")




# ---------------- CONFIG ----------------
st.set_page_config(page_title="Calendar", layout="centered")

FILE = "calendar_events.json"
today = date.today()

# ---------------- LOAD / SAVE ----------------
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
col1, col2 = st.columns(2)


with col1:
     LOCAL_TZ = ZoneInfo("Asia/Kolkata")  # Replace with your timezone, e.g. "Asia/Dubai"
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

# ---------------- DAY HEADERS ----------------
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
header_cols = st.columns(7)
for i, d in enumerate(days):
    header_cols[i].markdown(f"**{d}**")

# ---------------- CALENDAR GRID ----------------
cal = calendar.monthcalendar(year, month)

for week in cal:
    week_cols = st.columns(7)
    for i, day in enumerate(week):
        with week_cols[i]:
            if day == 0:
                st.write("")
            else:
                is_today = (
                    day == today.day
                    and month == today.month
                    and year == today.year
                )

                date_key = f"{year}-{month:02d}-{day:02d}"
                events = st.session_state.events.get(date_key, [])

                if is_today:
                    st.success(f"**{day}**")
                else:
                    st.markdown(f"**{day}**")

                for e in events:
                    st.write(f"• {e}")

# ---------------- YEAR COUNTDOWN ----------------
st.divider()
st.subheader("⏳ Year Countdown")

now = datetime.now(LOCAL_TZ)
end_of_year = datetime(year, 12, 31, 23, 59, 59, tzinfo=LOCAL_TZ)

diff_seconds = int((end_of_year - now).total_seconds())

if diff_seconds > 0:
    days, rem = divmod(diff_seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    st.info(
        f"🕒 {days} Days : {hours:02d} Hours : {minutes:02d} Minutes : {seconds:02d} Seconds"
    )
elif year == now.year:
    st.success("🎉 Happy New Year!")
else:
    st.warning("⚠️ Selected year has already ended")


# ---------------- ADD EVENT ----------------
st.divider()
st.subheader("➕ Add Event")

max_day = calendar.monthrange(year, month)[1]

c1, c2, c3 = st.columns(3)

with c1:
    event_day = st.number_input(
        "Day",
        min_value=1,
        max_value=max_day,
        value=min(today.day, max_day),
    )

with c2:
    event_text = st.text_input("Event")

with c3:
    add_btn = st.button("Add Event")

if add_btn:
    if event_text.strip():
        key = f"{year}-{month:02d}-{event_day:02d}"
        st.session_state.events.setdefault(key, []).append(event_text)
        save_events(st.session_state.events)
        st.success("Event added!")
        st.rerun()

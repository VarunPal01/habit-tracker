import streamlit as st
from datetime import date, timedelta
import matplotlib.pyplot as plt
from database import supabase

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Habit Tracker Pro",
    page_icon="🔥",
    layout="centered"
)

today = date.today()

# ---------------- STYLES ----------------
st.markdown("""
<style>
body { background-color: #020617; }
.habit-row { padding: 10px 4px; margin-bottom: 6px; }
.habit-name { font-size: 16px; font-weight: 600; }
.streak { color: #f97316; font-weight: 600; }
.sub { color: #94a3b8; font-size: 13px; }
hr { border: none; border-top: 1px solid #1e293b; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS (SUPABASE) ----------------
def get_habits():
    res = supabase.table("habits").select("name").execute()
    return [h["name"] for h in res.data]

def get_log(habit, d):
    res = supabase.table("habit_logs") \
        .select("completed") \
        .eq("habit", habit) \
        .eq("day", str(d)) \
        .execute()

    return bool(res.data[0]["completed"]) if res.data else False

def set_log(habit, d, value):
    supabase.table("habit_logs").upsert({
        "habit": habit,
        "day": str(d),
        "completed": int(value)
    }).execute()

def get_streak(habit):
    s = 0
    d = today
    while True:
        if get_log(habit, d):
            s += 1
            d -= timedelta(days=1)
        else:
            break
    return s

# ---------------- HEADER ----------------
st.markdown("## 🔥 Habit Tracker Pro")
st.markdown("<div class='sub'>Track habits • Build streaks • Stay consistent</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- ADD HABIT ----------------
c1, c2 = st.columns([8, 2])
with c1:
    new_habit = st.text_input("Add habit", label_visibility="collapsed")
with c2:
    if st.button("Add"):
        if new_habit:
            supabase.table("habits").insert({
                "name": new_habit
            }).execute()
            st.rerun()

# ---------------- TODAY ----------------
st.markdown(f"### 📅 Today — {today.strftime('%d/%m/%Y')}")

habits = get_habits()
completed_today = 0

if not habits:
    st.info("Add your first habit to start 🚀")

for habit in habits:
    checked = get_log(habit, today)

    st.markdown("<div class='habit-row'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([5, 2, 2, 1])

    c1.markdown(f"<div class='habit-name'>{habit}</div>", unsafe_allow_html=True)
  value = c2.checkbox(
    label="",
    value=checked,
    key=f"done_{habit}_{today.isoformat()}"
)

    c3.markdown(f"<div class='streak'>🔥 {get_streak(habit)} day(s)</div>", unsafe_allow_html=True)

    if c4.button("❌", key=f"del_{habit}"):
        supabase.table("habits").delete().eq("name", habit).execute()
        supabase.table("habit_logs").delete().eq("habit", habit).execute()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    set_log(habit, today, value)
    if value:
        completed_today += 1

# ---------------- PROGRESS ----------------
if habits:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📊 Daily Progress")
    st.progress(completed_today / len(habits))
    st.write(f"**{int((completed_today / len(habits)) * 100)}% completed**")

# ---------------- LAST 7 DAYS ----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 📊 Last 7 Days Overview")

total = 0
completed_7 = 0

for i in range(7):
    d = today - timedelta(days=i)
    for h in habits:
        total += 1
        if get_log(h, d):
            completed_7 += 1

missed_7 = total - completed_7

if total == 0:
    st.info("No data available")
else:
    fig, ax = plt.subplots()
    ax.pie(
        [completed_7, missed_7],
        labels=["Completed", "Missed"],
        autopct="%1.0f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

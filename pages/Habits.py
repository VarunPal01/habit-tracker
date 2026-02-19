import streamlit as st
from datetime import date, timedelta
import matplotlib.pyplot as plt
from supabase import create_client

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Habit Tracker",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- SUPABASE ----------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- AUTH ----------------
if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please login first")
    st.stop()

user_id = st.session_state.user_id
today = date.today()

# ---------------- STYLES ----------------
st.markdown("""
<style>
.habit { padding: 10px; border-radius: 12px; background: #0f172a; margin-bottom: 10px; }
.habit-name { font-weight: 600; font-size: 16px; }
.streak { color: #fb923c; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def get_habits():
    res = supabase.table("habits").select("name").eq("user_id", user_id).execute()
    return [h["name"] for h in res.data] if res.data else []

def get_log(habit, d):
    res = (
        supabase.table("habit_logs")
        .select("completed")
        .eq("habit", habit)
        .eq("day", str(d))
        .eq("user_id", user_id)
        .execute()
    )
    return bool(res.data and res.data[0]["completed"])

def set_log(habit, d, value):
    supabase.table("habit_logs").upsert({
        "habit": habit,
        "day": str(d),
        "completed": int(value),
        "user_id": user_id
    }).execute()

def get_streak(habit):
    s, d = 0, today
    while get_log(habit, d):
        s += 1
        d -= timedelta(days=1)
    return s

# ---------------- HEADER ----------------
st.title("🔥 Habit Tracker")
st.caption("Build consistency daily")
st.divider()

# ---------------- ADD HABIT ----------------
c1, c2 = st.columns([7, 3])

with c1:
    new_habit = st.text_input("New habit")

with c2:
    if st.button("Add"):
        if new_habit.strip():
            supabase.table("habits").insert({
                "name": new_habit.strip(),
                "user_id": user_id
            }).execute()
            st.rerun()

# ---------------- TODAY ----------------
st.subheader(f"📅 {today.strftime('%d %b %Y')}")

habits = get_habits()
done = 0

if not habits:
    st.info("Add your first habit")

for habit in habits:
    checked = get_log(habit, today)

    with st.container():
        st.markdown("<div class='habit'>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([6, 2, 2])

        c1.markdown(f"<div class='habit-name'>{habit}</div>", unsafe_allow_html=True)
        val = c2.checkbox("Done", value=checked, key=f"{habit}_{today}")
        c3.markdown(f"<div class='streak'>🔥 {get_streak(habit)}</div>", unsafe_allow_html=True)

        if st.button("❌", key=f"del_{habit}"):
            supabase.table("habits").delete().eq("name", habit).eq("user_id", user_id).execute()
            supabase.table("habit_logs").delete().eq("habit", habit).eq("user_id", user_id).execute()
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    set_log(habit, today, val)
    if val:
        done += 1

# ---------------- PROGRESS ----------------
if habits:
    st.divider()
    st.progress(done / len(habits))
    st.caption(f"{done} of {len(habits)} completed")

# ---------------- 7 DAY OVERVIEW ----------------
st.divider()
st.subheader("📊 Last 7 Days")

total = completed = 0
for i in range(7):
    d = today - timedelta(days=i)
    for h in habits:
        total += 1
        if get_log(h, d):
            completed += 1

if total > 0:
    fig, ax = plt.subplots()
    ax.pie([completed, total - completed], labels=["Done", "Missed"], autopct="%1.0f%%")
    st.pyplot(fig)
else:
    st.info("No data yet")

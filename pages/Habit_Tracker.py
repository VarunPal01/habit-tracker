import streamlit as st
import json, os
from datetime import date, timedelta
import matplotlib.pyplot as plt


# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Habit Tracker Pro",
    page_icon="🔥",
    layout="centered"
)

FILE = "database/habits.json"
today = date.today()

# ---------------- STYLE ----------------
st.markdown("""
<style>
body { background-color: #020617; }

.habit-row {
    padding: 10px 4px;
    margin-bottom: 6px;
}

.habit-name {
    font-size: 16px;
    font-weight: 600;
}

.streak {
    color: #f97316;
    font-weight: 600;
}

.sub {
    color: #94a3b8;
    font-size: 13px;
}

hr {
    border: none;
    border-top: 1px solid #1e293b;
    margin: 24px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def format_date(d):
    return d.strftime("%d/%m/%Y")

def load():
    if os.path.exists(FILE):
        with open(FILE) as f:
            return json.load(f)
    return {"habits": [], "data": {}}

def save(data):
    os.makedirs("database", exist_ok=True)
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def streak(habit, data):
    s, d = 0, today
    while data["data"].get(f"{d}_{habit}"):
        s += 1
        d -= timedelta(days=1)
    return s

# ---------------- STATE ----------------
if "db" not in st.session_state:
    st.session_state.db = load()

db = st.session_state.db

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
        if new_habit and new_habit not in db["habits"]:
            db["habits"].append(new_habit)
            save(db)
            st.rerun()

# ---------------- TODAY ----------------
st.markdown(f"### 📅 Today — {format_date(today)}")

completed = 0

if not db["habits"]:
    st.info("Add your first habit to start 🚀")

for habit in list(db["habits"]):
    key = f"{today}_{habit}"
    checked = db["data"].get(key, False)

    st.markdown("<div class='habit-row'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([5, 2, 2, 1])

    c1.markdown(f"<div class='habit-name'>{habit}</div>", unsafe_allow_html=True)
    value = c2.checkbox("Done", value=checked, key=key)
    c3.markdown(f"<div class='streak'>🔥 {streak(habit, db)} day(s)</div>", unsafe_allow_html=True)

    if c4.button("❌", key=f"del_{habit}"):
        db["habits"].remove(habit)
        db["data"] = {k: v for k, v in db["data"].items() if not k.endswith(f"_{habit}")}
        save(db)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    db["data"][key] = value
    if value:
        completed += 1

save(db)

# ---------------- PROGRESS ----------------
if db["habits"]:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("### 📊 Daily Progress")
    st.progress(completed / len(db["habits"]))
    st.write(f"**{int((completed/len(db['habits']))*100)}% completed**")

# ---------------- HISTORY ----------------
# ---------------- LAST 7 DAYS PIE CHART ----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### 📊 Last 7 Days Overview")

total = 0
completed_7 = 0

for i in range(7):
    d = today - timedelta(days=i)
    for h in db["habits"]:
        total += 1
        if db["data"].get(f"{d}_{h}"):
            completed_7 += 1

missed_7 = total - completed_7

if total == 0:
    st.info("No data available for last 7 days")
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

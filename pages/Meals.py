import streamlit as st
from datetime import date
from database.supabase_client import restore_session
from utils.auth_guard import require_login

st.set_page_config(
    page_title="Meal Tracker",
    page_icon="🍽️",
    layout="centered"
)

supabase = restore_session()
require_login()

user_id = st.session_state.user_id
today = date.today().isoformat()

st.title("🍽️ Meal Tracker")
st.caption("Track your daily meals")
st.divider()

for meal in ["Breakfast", "Lunch", "Dinner"]:
    food = st.text_input(f"{meal}")

    if st.button(f"Save {meal}", key=meal):
        if food.strip():
            supabase.table("meals").upsert({
                "user_id": user_id,
                "date": today,
                "meal": meal,
                "food": food
            }).execute()
            st.success(f"{meal} saved")
        else:
            st.warning("Food cannot be empty")

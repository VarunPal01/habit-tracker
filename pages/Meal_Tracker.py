import streamlit as st
import json
import os
from datetime import date

FILE = "database/meals.json"
today = date.today().isoformat()

def load_meals():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {}

def save_meals(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

if "meals" not in st.session_state:
    st.session_state.meals = load_meals()

meals = st.session_state.meals
meals.setdefault(today, {})

st.title("🍽️ Meal Tracker")
st.caption("Track what you eat daily")

st.divider()

for meal in ["Breakfast", "Lunch", "Dinner"]:
    st.subheader(meal)

    food = st.text_input(
        f"What did you eat for {meal}?",
        value=meals[today].get(meal, "")
    )

    meals[today][meal] = food

save_meals(meals)

st.success("Meals saved ✅")

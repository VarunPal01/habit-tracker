import streamlit as st
import json
import os
from datetime import datetime

# ---------- File to store data ----------
FILE = "budget_data.json"

# ---------- Load / Save Functions ----------
def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return {"income": [], "expenses": []}

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Main App ----------
st.set_page_config(page_title="Budget Tracker", layout="centered")
st.title("💰 Budget Tracker")

data = load_data()

# ---------- Add Income ----------
with st.expander("➕ Add Income"):
    income_amount = st.number_input("Income Amount", min_value=0.0, step=1.0, format="%.2f")
    income_source = st.text_input("Income Source")
    if st.button("Add Income"):
        if income_amount > 0 and income_source:
            data["income"].append({
                "amount": income_amount,
                "source": income_source,
                "date": str(datetime.now())
            })
            save_data(data)
            st.success("Income added successfully!")
        else:
            st.warning("Enter a valid amount and source!")

# ---------- Add Expense ----------
with st.expander("➕ Add Expense"):
    expense_amount = st.number_input("Expense Amount", min_value=0.0, step=1.0, format="%.2f", key="exp_amt")
    expense_category = st.text_input("Expense Category", key="exp_cat")
    if st.button("Add Expense"):
        if expense_amount > 0 and expense_category:
            data["expenses"].append({
                "amount": expense_amount,
                "category": expense_category,
                "date": str(datetime.now())
            })
            save_data(data)
            st.success("Expense added successfully!")
        else:
            st.warning("Enter a valid amount and category!")

# ---------- View Balance ----------
st.subheader("💵 Current Balance")
total_income = sum(item["amount"] for item in data["income"])
total_expense = sum(item["amount"] for item in data["expenses"])
balance = total_income - total_expense

st.write(f"**Total Income:** ₹{total_income}")
st.write(f"**Total Expenses:** ₹{total_expense}")
st.write(f"**Balance:** ₹{balance}")

# ---------- Expense Summary ----------
st.subheader("📊 Expense Summary by Category")
categories = {}
for expense in data["expenses"]:
    cat = expense["category"]
    categories[cat] = categories.get(cat, 0) + expense["amount"]

if categories:
    for cat, amt in categories.items():
        st.write(f"{cat}: ₹{amt}")
else:
    st.write("No expenses yet!")

# ---------- Show All Transactions ----------
st.subheader("📝 All Transactions")
st.write("**Income:**")
st.dataframe(data["income"])
st.write("**Expenses:**")
st.dataframe(data["expenses"])

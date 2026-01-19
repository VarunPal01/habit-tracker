import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# ------------------ Page Config ------------------
st.set_page_config(page_title="Budget Tracker", layout="centered")
st.title("💰 Budget Tracker")

# ------------------ Database Connection ------------------
conn = sqlite3.connect("budget.db", check_same_thread=False)
cursor = conn.cursor()

# ------------------ Create Tables ------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS income (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    source TEXT,
    date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    date TEXT
)
""")
conn.commit()

# ------------------ Add Income ------------------
with st.expander("➕ Add Income"):
    income_amount = st.number_input("Income Amount", min_value=0.0, step=1.0, format="%.2f")
    income_source = st.text_input("Income Source")

    if st.button("Add Income"):
        if income_amount > 0 and income_source.strip():
            cursor.execute(
                "INSERT INTO income (amount, source, date) VALUES (?, ?, ?)",
                (income_amount, income_source, str(datetime.now()))
            )
            conn.commit()
            st.success("Income added successfully!")
        else:
            st.warning("Please enter valid income details.")

# ------------------ Add Expense ------------------
with st.expander("➕ Add Expense"):
    expense_amount = st.number_input(
        "Expense Amount", min_value=0.0, step=1.0, format="%.2f", key="exp_amt"
    )
    expense_category = st.text_input("Expense Category", key="exp_cat")

    if st.button("Add Expense"):
        if expense_amount > 0 and expense_category.strip():
            cursor.execute(
                "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
                (expense_amount, expense_category, str(datetime.now()))
            )
            conn.commit()
            st.success("Expense added successfully!")
        else:
            st.warning("Please enter valid expense details.")

# ------------------ Current Balance ------------------
st.subheader("💵 Current Balance")

cursor.execute("SELECT SUM(amount) FROM income")
total_income = cursor.fetchone()[0] or 0

cursor.execute("SELECT SUM(amount) FROM expenses")
total_expense = cursor.fetchone()[0] or 0

balance = total_income - total_expense

st.write(f"**Total Income:** ₹{total_income}")
st.write(f"**Total Expenses:** ₹{total_expense}")
st.write(f"**Balance:** ₹{balance}")

# ------------------ Expense Summary ------------------
st.subheader("📊 Expense Summary by Category")

cursor.execute("""
SELECT category, SUM(amount)
FROM expenses
GROUP BY category
""")

rows = cursor.fetchall()

if rows:
    for cat, amt in rows:
        st.write(f"{cat}: ₹{amt}")
else:
    st.write("No expenses yet!")

# ------------------ Show All Transactions ------------------
st.subheader("📝 All Transactions")

cursor.execute("SELECT amount, source, date FROM income ORDER BY date DESC")
income_data = cursor.fetchall()

cursor.execute("SELECT amount, category, date FROM expenses ORDER BY date DESC")
expense_data = cursor.fetchall()

st.write("**Income**")
if income_data:
    df_income = pd.DataFrame(income_data, columns=["Amount", "Source", "Date"])
    st.dataframe(df_income, use_container_width=True)
else:
    st.write("No income records.")

st.write("**Expenses**")
if expense_data:
    df_expense = pd.DataFrame(expense_data, columns=["Amount", "Category", "Date"])
    st.dataframe(df_expense, use_container_width=True)
else:
    st.write("No expense records.")

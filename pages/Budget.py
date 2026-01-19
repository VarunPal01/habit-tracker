import streamlit as st
import pandas as pd
from supabase import create_client

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Budget Tracker",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- SUPABASE ----------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------- AUTH GUARD ----------------
if "user_id" not in st.session_state or st.session_state.user_id is None:
    st.warning("Please login first")
    st.stop()

user_id = st.session_state.user_id

# ---------------- HEADER ----------------
st.title("💰 Budget Tracker")
st.caption("Track your income and expenses")

st.divider()

# ---------------- ADD INCOME ----------------
with st.expander("➕ Add Income"):
    inc_amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0,
        key="inc_amt"
    )
    inc_source = st.text_input("Source", key="inc_src")

    if st.button("Add Income"):
        if inc_amount > 0 and inc_source.strip():
            supabase.table("income").insert({
                "amount": inc_amount,
                "source": inc_source,
                "user_id": user_id
            }).execute()
            st.success("Income added ✅")
            st.rerun()
        else:
            st.warning("Enter valid income details")

# ---------------- ADD EXPENSE ----------------
with st.expander("➖ Add Expense"):
    exp_amount = st.number_input(
        "Amount",
        min_value=0.0,
        step=1.0,
        key="exp_amt"
    )
    exp_category = st.text_input("Category", key="exp_cat")

    if st.button("Add Expense"):
        if exp_amount > 0 and exp_category.strip():
            supabase.table("expenses").insert({
                "amount": exp_amount,
                "category": exp_category,
                "user_id": user_id
            }).execute()
            st.success("Expense added ✅")
            st.rerun()
        else:
            st.warning("Enter valid expense details")

st.divider()

# ---------------- FETCH DATA ----------------
income = (
    supabase
    .table("income")
    .select("amount, source, created_at")
    .eq("user_id", user_id)
    .order("created_at", desc=True)
    .execute()
).data or []

expenses = (
    supabase
    .table("expenses")
    .select("amount, category, created_at")
    .eq("user_id", user_id)
    .order("created_at", desc=True)
    .execute()
).data or []

# ---------------- CALCULATIONS ----------------
total_income = sum(i["amount"] for i in income)
total_expense = sum(e["amount"] for e in expenses)
balance = total_income - total_expense

# ---------------- METRICS (MOBILE FRIENDLY) ----------------
st.subheader("💵 Overview")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Income", f"₹ {total_income}")

with c2:
    st.metric("Expenses", f"₹ {total_expense}")

with c3:
    st.metric("Balance", f"₹ {balance}")

st.divider()

# ---------------- TRANSACTIONS ----------------
st.subheader("📄 Transactions")

if not income and not expenses:
    st.info("No transactions yet")
else:
    if income:
        st.markdown("**Income**")
        st.dataframe(
            pd.DataFrame(income),
            use_container_width=True,
            hide_index=True
        )

    if expenses:
        st.markdown("**Expenses**")
        st.dataframe(
            pd.DataFrame(expenses),
            use_container_width=True,
            hide_index=True
        )

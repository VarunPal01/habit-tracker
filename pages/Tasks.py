import streamlit as st
from database.supabase_client import restore_session
from utils.auth_guard import require_login

st.set_page_config(
    page_title="Tasks",
    page_icon="📌",
    layout="centered"
)

supabase = restore_session()
require_login()

user_id = st.session_state.user_id

st.title("📌 Tasks")
st.caption("Simple daily task list")
st.divider()

task = st.text_input("Add new task")

if st.button("Add Task"):
    if task.strip():
        supabase.table("tasks").insert({
            "user_id": user_id,
            "task": task
        }).execute()
        st.rerun()

tasks = (
    supabase
    .table("tasks")
    .select("*")
    .eq("user_id", user_id)
    .execute()
).data or []

if not tasks:
    st.info("No tasks yet")
else:
    for t in tasks:
        col1, col2 = st.columns([8, 2])
        col1.write(t["task"])
        if col2.button("Done", key=t["id"]):
            supabase.table("tasks").delete().eq("id", t["id"]).execute()
            st.rerun(
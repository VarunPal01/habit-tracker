import streamlit as st
from database.supabase_client import restore_session
from utils.auth_guard import require_login

# ---------------- AUTH ----------------
supabase = restore_session()
require_login()

user_id = st.session_state.user_id

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Vision Board",
    page_icon="🌈",
    layout="centered"
)

# ---------------- LOAD VISION ----------------
def load_vision():
    res = (
        supabase
        .table("vision")
        .select("text")
        .eq("user_id", user_id)
        .execute()
    )

    if res.data:
        return res.data[0]["text"]

    return ""  # no vision yet

# ---------------- SAVE VISION ----------------
def save_vision(text):
    supabase.table("vision").upsert({
        "user_id": user_id,
        "text": text
    }).execute()

# ---------------- UI ----------------
st.title("🌈 Vision Board")
st.caption("Write your goals, dreams, and future plans")
st.divider()

vision_text = st.text_area(
    "Your Vision",
    value=load_vision(),
    height=260,
    placeholder=(
        "Example:\n"
        "• Become disciplined\n"
        "• Build my own startup\n"
        "• Stay consistent with habits"
    )
)

if st.button("💾 Save Vision", use_container_width=True):
    if vision_text.strip():
        save_vision(vision_text.strip())
        st.success("Vision saved successfully ✅")
    else:
        st.warning("Vision cannot be empty")

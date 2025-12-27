import streamlit as st
import json
import os

st.set_page_config(page_title="Vision Board", layout="centered")

VISION_FILE = "vision.txt"

# ---------- LOAD VISION ----------
def load_vision():
    if os.path.exists(VISION_FILE):
        with open(VISION_FILE, "r") as f:
            return f.read()
    return ""

# ---------- SAVE VISION ----------
def save_vision(text):
    with open(VISION_FILE, "w") as f:
        f.write(text)

st.title("🌈 Vision Board")
st.write("Write your dreams, goals, and future plans")

st.divider()

vision_text = st.text_area(
    "Your Vision",
    value=load_vision(),
    height=250,
    placeholder="Example:\n• Become disciplined\n• Learn Python deeply\n• Get a good job"
)

if st.button("💾 Save Vision"):
    if vision_text.strip():
        save_vision(vision_text)
        st.success("Vision saved successfully ✅")
    else:
        st.warning("Vision cannot be empty")

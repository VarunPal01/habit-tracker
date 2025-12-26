import streamlit as st

st.set_page_config(page_title="Vision Board", layout="centered")

st.title("🌈 Vision Board")
st.write("This page is for your dreams and goals")

st.divider()

vision_text = st.text_area(
    "Write your vision / goals",
    placeholder="Example:\n• Become fit\n• Learn Python\n• Get a good job"
)

if st.button("Save Vision"):
    if vision_text.strip():
        st.success("Vision saved (temporary).")
    else:
        st.warning("Please write something")

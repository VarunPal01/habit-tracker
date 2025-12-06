import streamlit as st
import pandas as pd

st.title("My Habit Tracker")

# Initialize storage
if "habits" not in st.session_state:
    st.session_state.habits = []

# Add habit input
habit = st.text_input("Enter a habit:")
if st.button("Add Habit"):
    if habit.strip():  # avoid empty input
        st.session_state.habits.append({"Habit": habit})
        st.success(f"Added habit: {habit}")

st.subheader("Your Habits")

# Show only if habits exist
if st.session_state.habits:
    df = pd.DataFrame(st.session_state.habits)

    # Add Serial Numbers starting from 1
    df.index = df.index + 1
    df.reset_index(inplace=True)
    df.rename(columns={"index": "S.No"}, inplace=True)

    # Display table with checkboxes
    st.write("Tick when completed:")

    remove_list = []  # store completed habits

    for i, row in df.iterrows():
        col1, col2, col3 = st.columns([1,5,1])
        col1.write(row["S.No"])
        col2.write(row["Habit"])
        done = col3.checkbox("Done", key=f"done_{row['S.No']}")

        if done:
            remove_list.append(row["Habit"])

    # Remove checked habits
    if remove_list:
        for h in remove_list:
            st.session_state.habits = [item for item in st.session_state.habits if item["Habit"] != h]
        st.rerun()
else:
    st.info("No habits added yet.")



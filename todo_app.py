import streamlit as st

st.title("📋 ToDo List App")

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Add new task
with st.form("Add task"):
    new_task = st.text_input("Enter new task:")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks.append(new_task.strip())

st.subheader("✅ Current Tasks")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        col1, col2, col3, col4, col5 = st.columns([6,1,1,1,1])
        col1.markdown(f"**{i+1}. {task}**")
        if col2.button("✅", key=f"done_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
        if col3.button("❌", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
        if col4.button("⬆️", key=f"up_{i}") and i > 0:
            st.session_state.tasks[i], st.session_state.tasks[i-1] = st.session_state.tasks[i-1], st.session_state.tasks[i]
            st.experimental_rerun()
        if col5.button("⬇️", key=f"down_{i}") and i < len(st.session_state.tasks)-1:
            st.session_state.tasks[i], st.session_state.tasks[i+1] = st.session_state.tasks[i+1], st.session_state.tasks[i]
            st.experimental_rerun()
else:
    st.info("No tasks yet. Add a task above!")

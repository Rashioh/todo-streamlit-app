import streamlit as st

st.set_page_config(page_title="📋 ToDo List App", page_icon="✅")
st.title("📋 ToDo List App")

# Initialize task list
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# Add new task
with st.form("Add task", clear_on_submit=True):
    new_task = st.text_input("Enter new task")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks.append(new_task.strip())

st.subheader("✅ Current Tasks")

# Show tasks
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([7,1,1,1,1])
        cols[0].markdown(f"**{i+1}. {task}**")

        # Define separate buttons for each action, with unique keys
        if cols[1].button("✅", key=f"done_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
        if cols[2].button("❌", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
        if cols[3].button("⬆️", key=f"up_{i}"):
            if i > 0:
                st.session_state.tasks[i-1], st.session_state.tasks[i] = st.session_state.tasks[i], st.session_state.tasks[i-1]
                st.experimental_rerun()
        if cols[4].button("⬇️", key=f"down_{i}"):
            if i < len(st.session_state.tasks)-1:
                st.session_state.tasks[i+1], st.session_state.tasks[i] = st.session_state.tasks[i], st.session_state.tasks[i+1]
                st.experimental_rerun()
else:
    st.info("No tasks yet. Add one above!")

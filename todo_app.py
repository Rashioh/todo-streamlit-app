import streamlit as st

st.set_page_config(page_title="📋 ToDo List App", page_icon="✅")
st.title("📋 ToDo List App")

# Initialize task list and action flags
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'action' not in st.session_state:
    st.session_state.action = None
if 'action_index' not in st.session_state:
    st.session_state.action_index = None

# Add new task
with st.form("Add task", clear_on_submit=True):
    new_task = st.text_input("Enter new task")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks.append(new_task.strip())

st.subheader("✅ Current Tasks")

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([7,1,1,1,1])
        cols[0].markdown(f"**{i+1}. {task}**")
        if cols[1].button("✅", key=f"done_{i}"):
            st.session_state.action = 'done'
            st.session_state.action_index = i
        if cols[2].button("❌", key=f"delete_{i}"):
            st.session_state.action = 'delete'
            st.session_state.action_index = i
        if cols[3].button("⬆️", key=f"up_{i}"):
            st.session_state.action = 'up'
            st.session_state.action_index = i
        if cols[4].button("⬇️", key=f"down_{i}"):
            st.session_state.action = 'down'
            st.session_state.action_index = i
else:
    st.info("No tasks yet. Add one above!")

# Apply action outside the loop
if st.session_state.action is not None:
    idx = st.session_state.action_index
    if st.session_state.action in ['done', 'delete']:
        if 0 <= idx < len(st.session_state.tasks):
            st.session_state.tasks.pop(idx)
    elif st.session_state.action == 'up':
        if idx > 0:
            st.session_state.tasks[idx], st.session_state.tasks[idx-1] = st.session_state.tasks[idx-1], st.session_state.tasks[idx]
    elif st.session_state.action == 'down':
        if idx < len(st.session_state.tasks)-1:
            st.session_state.tasks[idx], st.session_state.tasks[idx+1] = st.session_state.tasks[idx+1], st.session_state.tasks[idx]
    # Reset action
    st.session_state.action = None
    st.session_state.action_index = None
    st.experimental_rerun()

import streamlit as st
import json
import os

st.set_page_config(page_title="📋 ToDo List App", page_icon="✅")
st.title("📋 ToDo List App")

TASKS_FILE = "tasks.json"

# Load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

# Initialize task list in session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_tasks()

# --- Add new task ---
st.subheader("➕ Add a new task")
with st.form("Add task", clear_on_submit=True):
    new_task = st.text_input("Enter new task:")
    submitted = st.form_submit_button("Add Task")
    if submitted and new_task.strip():
        st.session_state.tasks.append(new_task.strip())
        save_tasks(st.session_state.tasks)

# --- Show current tasks ---
st.subheader("✅ Your Tasks")

action = None
index = None

if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.7, 0.07, 0.07, 0.07, 0.07])
        cols[0].markdown(f"**{i+1}. {task}**")
        with cols[1]:
            if st.button("✅", key=f"done_{i}"):
                action = 'done'
                index = i
                break
        with cols[2]:
            if st.button("❌", key=f"delete_{i}"):
                action = 'delete'
                index = i
                break
        with cols[3]:
            if st.button("⬆️", key=f"up_{i}") and i > 0:
                action = 'up'
                index = i
                break
        with cols[4]:
            if st.button("⬇️", key=f"down_{i}") and i < len(st.session_state.tasks)-1:
                action = 'down'
                index = i
                break

    # Apply action
    if action in ['done', 'delete']:
        st.session_state.tasks.pop(index)
        save_tasks(st.session_state.tasks)
    elif action == 'up':
        st.session_state.tasks[index], st.session_state.tasks[index-1] = (
            st.session_state.tasks[index-1], st.session_state.tasks[index])
        save_tasks(st.session_state.tasks)
    elif action == 'down':
        st.session_state.tasks[index], st.session_state.tasks[index+1] = (
            st.session_state.tasks[index+1], st.session_state.tasks[index])
        save_tasks(st.session_state.tasks)

else:
    st.info("No tasks yet. Add your first task above!")

st.markdown("---")
st.caption("✨ Simple, persistent ToDo list built with Streamlit")

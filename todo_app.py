import streamlit as st
import json
import os

st.set_page_config(page_title="📋 ToDo List App", page_icon="✅")

TASKS_FILE = "tasks.json"
DONE_FILE = "done_tasks.json"

# Functions to load & save lists
def load_list(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_list(lst, file):
    with open(file, "w") as f:
        json.dump(lst, f)

# Initialize session state
if 'tasks' not in st.session_state:
    st.session_state.tasks = load_list(TASKS_FILE)
if 'done_tasks' not in st.session_state:
    st.session_state.done_tasks = load_list(DONE_FILE)

st.title("📋 Simple ToDo List App")

# Add new task
new_task = st.text_input("Enter a new task:")
if st.button("➕ Add Task"):
    task_text = new_task.strip()
    if task_text:
        st.session_state.tasks.append(task_text)
        save_list(st.session_state.tasks, TASKS_FILE)

# Show current tasks
st.subheader("✅ Your Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, 1):
        st.markdown(f"**{i}. {task}**")
else:
    st.info("No tasks yet. Add one above!")

# Select and edit task
if st.session_state.tasks:
    st.subheader("✏️ Edit Selected Task")
    selected_task = st.selectbox("Select task to edit:", options=st.session_state.tasks)

    col_done, col_delete = st.columns(2)

    if col_done.button("✅ Mark as Done"):
        st.session_state.done_tasks.append(selected_task)
        st.session_state.tasks.remove(selected_task)
        save_list(st.session_state.tasks, TASKS_FILE)
        save_list(st.session_state.done_tasks, DONE_FILE)

    if col_delete.button("❌ Delete Task"):
        st.session_state.tasks.remove(selected_task)
        save_list(st.session_state.tasks, TASKS_FILE)

# Show done tasks
st.subheader("🎉 Done Tasks")
if st.session_state.done_tasks:
    for i, task in enumerate(st.session_state.done_tasks, 1):
        st.markdown(f"{i}. {task}")
    # Select done task to delete
    selected_done_task = st.selectbox("Select done task to delete:", options=st.session_state.done_tasks, key="done_task_select")
    if st.button("🗑️ Delete from Done"):
        st.session_state.done_tasks.remove(selected_done_task)
        save_list(st.session_state.done_tasks, DONE_FILE)
else:
    st.write("No tasks marked as done yet.")

st.caption("✨ Simple ToDo list built with Streamlit")

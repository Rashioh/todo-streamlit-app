import streamlit as st
import json
import os

st.set_page_config(page_title="📋 ToDo List App", page_icon="✅")

TASKS_FILE = "tasks.json"
DONE_FILE = "done_tasks.json"

def load_list(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return []

def save_list(lst, file):
    with open(file, "w") as f:
        json.dump(lst, f)

if 'tasks' not in st.session_state:
    st.session_state.tasks = load_list(TASKS_FILE)
if 'done_tasks' not in st.session_state:
    st.session_state.done_tasks = load_list(DONE_FILE)

st.title("📋 Simple ToDo List App")

# Add new task
new_task = st.text_input("Enter a new task:")
if st.button("➕ Add Task"):
    if new_task.strip():
        st.session_state.tasks.append(new_task.strip())
        save_list(st.session_state.tasks, TASKS_FILE)

# Show current tasks
st.subheader("✅ Your Tasks")
if st.session_state.tasks:
    for i, task in enumerate(st.session_state.tasks, 1):
        st.markdown(f"**{i}. {task}**")
else:
    st.info("No tasks yet. Add one above!")

# Select task to edit
if st.session_state.tasks:
    st.subheader("✏️ Edit Task")
    selected_task = st.selectbox("Select task:", options=st.session_state.tasks)
    
    col_done, col_del = st.columns(2)
    
    if col_done.button("✅ Mark as Done"):
        st.session_state.done_tasks.append(selected_task)
        save_list(st.session_state.done_tasks, DONE_FILE)
        st.session_state.tasks.remove(selected_task)
        save_list(st.session_state.tasks, TASKS_FILE)
        st.experimental_rerun()  # Refresh UI
    
    if col_del.button("❌ Delete Task"):
        st.session_state.tasks.remove(selected_task)
        save_list(st.session_state.tasks, TASKS_FILE)
        st.experimental_rerun()  # Refresh UI

# Show done tasks
st.subheader("🎉 Done Tasks")
if st.session_state.done_tasks:
    for j, task in enumerate(st.session_state.done_tasks, 1):
        st.write(f"{j}. {task}")
else:
    st.write("No tasks marked as done yet.")

st.caption("✨ Simple web ToDo list built with Streamlit")

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

if st.session_state.tasks:
    # Number and display tasks
    for i, task in enumerate(st.session_state.tasks):
        st.markdown(f"**{i+1}. {task}**")

    # Select task to edit
    selected_index = st.selectbox(
        "Select task to edit:", 
        options=list(range(len(st.session_state.tasks))),
        format_func=lambda x: f"{x+1}. {st.session_state.tasks[x]}"
    )

    # One set of action buttons
    cols = st.columns(5)
    if cols[0].button("✅ Mark Done"):
        st.session_state.tasks.pop(selected_index)
        save_tasks(st.session_state.tasks)
    if cols[1].button("❌ Delete"):
        st.session_state.tasks.pop(selected_index)
        save_tasks(st.session_state.tasks)
    if cols[2].button("⬆️ Move Up") and selected_index > 0:
        st.session_state.tasks[selected_index], st.session_state.tasks[selected_index - 1] = (
            st.session_state.tasks[selected_index - 1], st.session_state.tasks[selected_index])
        save_tasks(st.session_state.tasks)
    if cols[3].button("⬇️ Move Down") and selected_index < len(st.session_state.tasks) - 1:
        st.session_state.tasks[selected_index], st.session_state.tasks[selected_index + 1] = (
            st.session_state.tasks[selected_index + 1], st.session_state.tasks[selected_index])
        save_tasks(st.session_state.tasks)
    if cols[4].button("✏️ Edit"):
        new_text = st.text_input("Edit task text:", value=st.session_state.tasks[selected_index], key='edit_text')
        if new_text.strip():
            st.session_state.tasks[selected_index] = new_text.strip()
            save_tasks(st.session_state.tasks)

else:
    st.info("No tasks yet. Add your first task above!")

st.markdown("---")
st.caption("✨ Simple, persistent ToDo list built with Streamlit")

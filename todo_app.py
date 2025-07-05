import json
import ipywidgets as widgets
from IPython.display import display, clear_output

# Files
done_file = "done_tasks.json"

# Try to load saved tasks, or start fresh
try:
    with open("tasks.json", "r") as f:
        tasks = json.load(f)
except:
    tasks = []

# Widgets
task_input = widgets.Text(placeholder='Enter a task')
add_button = widgets.Button(description="Add Task", button_style='success')
delete_dropdown = widgets.Dropdown(options=[], description='Delete:')
delete_button = widgets.Button(description="Delete", button_style='danger')
done_dropdown = widgets.Dropdown(options=[], description='Done:')
done_button = widgets.Button(description="Mark as Done", button_style='info')
output = widgets.Output()

def save_tasks():
    with open("tasks.json", "w") as f:
        json.dump(tasks, f)

def save_done_task(task_text):
    try:
        with open(done_file, "r") as f:
            done_tasks = json.load(f)
    except:
        done_tasks = []
    done_tasks.append(task_text)
    with open(done_file, "w") as f:
        json.dump(done_tasks, f)

def refresh_dropdowns():
    delete_dropdown.options = tasks
    done_dropdown.options = tasks

def show_lists():
    with output:
        clear_output()
        print("📋 ToDo List:")
        if tasks:
            for i, text in enumerate(tasks, 1):
                print(f"{i}. {text}")
        else:
            print("No tasks yet.")

def on_add_clicked(b):
    text = task_input.value.strip()
    if text:
        tasks.append(text)
        task_input.value = ''
        save_tasks()
        refresh_dropdowns()
        show_lists()

def on_delete_clicked(b):
    if delete_dropdown.options:
        index = delete_dropdown.index
        tasks.pop(index)
        save_tasks()
        refresh_dropdowns()
        show_lists()

def on_done_clicked(b):
    if done_dropdown.options:
        index = done_dropdown.index
        task = tasks.pop(index)
        save_done_task(task)
        save_tasks()
        refresh_dropdowns()
        show_lists()

# Bind events
add_button.on_click(on_add_clicked)
delete_button.on_click(on_delete_clicked)
done_button.on_click(on_done_clicked)

# Display interface
display(widgets.VBox([
    widgets.HBox([task_input, add_button]),
    widgets.HBox([delete_dropdown, delete_button]),
    widgets.HBox([done_dropdown, done_button]),
    output
]))

# Initial display
refresh_dropdowns()
show_lists()

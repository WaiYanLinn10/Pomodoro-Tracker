import csv

TASK_FILE = "tasks.csv"

def read_tasks():
    with open(TASK_FILE, newline="") as file:
        return list(csv.DictReader(file))

def write_tasks(tasks):
    with open(TASK_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=tasks[0].keys())
        writer.writeheader()
        writer.writerows(tasks)

def add_task(name, category, estimated):
    tasks = read_tasks()

    for task in tasks:
        if task["task_name"].lower() == name.lower():
            print(f"Task '{name}' already exists!")
            return
        
    tasks.append({
        "task_name": name,
        "category": category,
        "estimated_pomodoros": estimated,
        "completed_pomodoros": 0,
        "status": "not started"
    })
    write_tasks(tasks)

def complete_pomodoro(task_name):
    tasks = read_tasks()

    for task in tasks:
        if task["task_name"] == task_name:
            task["completed_pomodoros"] = int(task["completed_pomodoros"]) + 1
            task["status"] = "in progress"

            if int(task["completed_pomodoros"]) >= int(task["estimated_pomodoros"]):
                task["status"] = "completed"

    write_tasks(tasks)

import csv
from datetime import date

Task_File = "tasks.csv"
Pomodoro_File = "count_pomodoro.csv"

def read_tasks():
    with open(Task_File, newline="") as file:
        return list(csv.DictReader(file))

def write_tasks(tasks):
    with open(Task_File, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=tasks[0].keys())
        writer.writeheader()
        writer.writerows(tasks)

def add_task(name, category, estimated,due_date):
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
        "status": "not started",
        "start_date": date.today(),
        "due_date": due_date, 
        "end_date": ""
    })
    write_tasks(tasks)

def complete_pomodoro(task_name):
    tasks = read_tasks()
    today = date.today().isoformat()

    for task in tasks:
        if task["task_name"] == task_name:
            task["completed_pomodoros"] = int(task["completed_pomodoros"]) + 1
            task["status"] = "in progress"

            if int(task["completed_pomodoros"]) >= int(task["estimated_pomodoros"]):
                task["status"] = "completed"
                task["end_date"] = date.today().isoformat()

    write_tasks(tasks)
    log_pomodoro(task_name)


def show_tasks():
    tasks = read_tasks()

    if not tasks:
        print("No tasks available.")
        return

    print("\nCurrent Tasks:")
    for task in tasks:
        print(
            f"- {task['task_name']} | "
            f"{task['completed_pomodoros']}/{task['estimated_pomodoros']} | "
            f"{task['status']}"
        )

def select_task():
    tasks = read_tasks()
    if not tasks:
        print("No tasks available.")
        return None

    print("\nSelect a task:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task['task_name']} ({task['status']})")

    while True:
        choice = input("Enter task number: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(tasks):
                return tasks[choice - 1]['task_name']
        print("Invalid choice, try again")

def check_task_status(task_name):
    tasks = read_tasks()
    for task in tasks:
        if task["task_name"] == task_name:
            return task["status"] == "completed"
    return False

def log_pomodoro(task_name):
    with open(Pomodoro_File, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date.today().isoformat(), task_name])

def pomodoros_count():
    today = date.today().isoformat()
    count = 0

    try:
        with open(Pomodoro_File, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == today:
                    count += 1
    except FileNotFoundError:
        pass

    return count

import csv
from datetime import date

TASK_FILE = "tasks.csv"

def daily_summary():
    total = 0

    with open(TASK_FILE, newline="") as file:
        reader = csv.DictReader(file)
        for task in reader:
            total += int(task["completed_pomodoros"])

    print("Daily Summary")
    print(f"Pomodoros completed today: {total}")
    print(f"Focused time: {total * 25} minutes")

import csv
from datetime import date
import os

class Task:
    def __init__(self, name, category, estimated_pomodoros, due_date, completed_pomodoros=0, status="not started", start_date=None, end_date=""):
        self.name = name
        self.category = category
        self.estimated_pomodoros = int(estimated_pomodoros)
        self.completed_pomodoros = int(completed_pomodoros)
        self.due_date = due_date
        self.status = status
        self.start_date = start_date if start_date else date.today().isoformat()
        self.end_date = end_date

    def mark_completed(self):
        self.status = "completed"
        self.end_date = date.today().isoformat()

    def add_pomodoro(self):
        self.completed_pomodoros += 1
        self.status = "in progress"
        if self.completed_pomodoros >= self.estimated_pomodoros:
            self.mark_completed()

    def is_completed(self):
        return self.status == "completed"

    def to_dict(self):
        return {
            "task_name": self.name,
            "category": self.category,
            "estimated_pomodoros": self.estimated_pomodoros,
            "completed_pomodoros": self.completed_pomodoros,
            "status": self.status,
            "start_date": self.start_date,
            "due_date": self.due_date,
            "end_date": self.end_date
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["task_name"],
            category=data["category"],
            estimated_pomodoros=data["estimated_pomodoros"],
            due_date=data["due_date"],
            completed_pomodoros=data["completed_pomodoros"],
            status=data["status"],
            start_date=data.get("start_date"),
            end_date=data.get("end_date", "")
        )


class TaskManager:
    TASK_FILE = "tasks.csv"
    POMODORO_FILE = "count_pomodoro.csv"

    def __init__(self):
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        if not os.path.exists(self.TASK_FILE):
            return
        
        with open(self.TASK_FILE, newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.tasks.append(Task.from_dict(row))

    def save_tasks(self):
        if not self.tasks:
            return

        with open(self.TASK_FILE, "w", newline="") as file:
            fieldnames = self.tasks[0].to_dict().keys()
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow(task.to_dict())

    def add_task(self, name, category, estimated, due_date):
        try:
            due = date.fromisoformat(due_date)
            today = date.today()

            if due < today:
                return False, "Due date must be today or later."
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD."

        if self.get_task_by_name(name):
            return False, f"Task '{name}' already exists!"

        new_task = Task(name, category, estimated, due_date)
        self.tasks.append(new_task)
        self.save_tasks()

        return True, "Task added successfully."

    
    def delete_task(self, task_name):
        task = self.get_task_by_name(task_name)

        if not task:
            return False, f"Task '{task_name}' not found."

        self.tasks.remove(task)

        if not self.tasks:
            with open(self.TASK_FILE, "w", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=task.to_dict().keys()
                )
                writer.writeheader()
            return True, f"Task '{task_name}' deleted. No tasks remaining."

        self.save_tasks()
        return True, f"Task '{task_name}' deleted successfully."

    def get_task_by_name(self, name):
        for task in self.tasks:
            if task.name.lower() == name.lower():
                return task
        return None

    def get_all_tasks(self):
        return self.tasks

    def get_todays_pomodoro_count(self):
        today = date.today().isoformat()
        count = 0
        if not os.path.exists(self.POMODORO_FILE):
            return 0
            
        with open(self.POMODORO_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == today:
                    count += 1
        return count

    def log_pomodoro(self, task_name):
        task = self.get_task_by_name(task_name)

        if not task:
            return False, "Task not found."

        task.add_pomodoro()
        self.save_tasks()

        with open(self.POMODORO_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date.today().isoformat(), task_name])

        return True, "Pomodoro recorded successfully."

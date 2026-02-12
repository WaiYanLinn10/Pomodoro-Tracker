from datetime import datetime, date
from timer import PomodoroTimer
from task import TaskManager


def show_tasks_ui(manager):
    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks available.")
        return

    print("\nCurrent Tasks:")
    for task in tasks:
        print(
            f"- {task.name} | "
            f"{task.completed_pomodoros}/{task.estimated_pomodoros} | "
            f"{task.status}"
        )


def select_task_ui(manager):
    tasks = manager.get_all_tasks()
    if not tasks:
        print("No tasks available.")
        return None

    print("\nSelect a task:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task.name} ({task.status})")

    while True:
        choice = input("Enter task number: ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(tasks):
                return tasks[choice - 1].name
        print("Invalid choice, try again")


def main():
    timer = PomodoroTimer()
    manager = TaskManager()

    while True:
        print("\n--- Pomodoro Task Manager ---")
        print("1. Add new task")
        print("2. Start Pomodoro")
        print("3. Complete Pomodoro for a task")
        print("4. Show tasks")
        print("5. Delete task")
        print("6. Daily summary")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Task name: ")
            category = input("Category: ")
            while True:
                estimated = input("Estimated Pomodoros (>= 1): ").strip()
                if estimated.isdigit() and int(estimated) >= 1:
                    estimated = int(estimated)
                    break
                print("Please enter a whole number (1 or more).")

            while True:
                due_date = input("Due date (YYYY-MM-DD): ").strip()

                try:
                    parsed_date = datetime.strptime(due_date, "%Y-%m-%d").date()

                    if parsed_date < date.today():
                        print("Due date must be today or later.")
                        continue

                    break 

                except ValueError:
                    print("Invalid format. Please use YYYY-MM-DD.")

            print("Task added")
            success, message = manager.add_task(name, category, estimated, due_date)
            print(message)

        elif choice == "2":
            timer.start()

        elif choice == "3":
            task_name = select_task_ui(manager)

            if task_name:
                while True:
                    task = manager.get_task_by_name(task_name)
                    if task.is_completed():
                        print(f"Task '{task_name}' is already completed.")
                        break

                    timer.start()
                    timer.complete()
                    manager.log_pomodoro(task_name)
                    print(f"Pomodoro for '{task_name}' completed and recorded")

                    study_again = input(
                        "Start another Pomodoro for this task? (y/n): "
                    ).lower()
                    if study_again != "y":
                        break

        elif choice == "4":
            show_tasks_ui(manager)

        elif choice == "5":
            task_name = select_task_ui(manager)
            if task_name:
                confirm = input(
                    f"Are you sure you want to delete '{task_name}'? (y/n): "
                ).lower()
                if confirm == "y":
                    success, message = manager.delete_task(task_name)
                    print(message)
                else:
                    print("Delete cancelled.")

        elif choice == "6":
            today_pomodoros_count = manager.get_todays_pomodoro_count()
            print(f"Pomodoros completed today: {today_pomodoros_count}")
            print(f"Focus time today: {today_pomodoros_count * 25} minutes")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()

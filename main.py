from timer import PomodoroTimer
from task import add_task, complete_pomodoro, read_tasks
from report import daily_summary

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

def main():
    timer = PomodoroTimer()

    while True:
        print("\n--- Pomodoro Task Manager ---")
        print("1. Add new task")
        print("2. Start Pomodoro")
        print("3. Complete Pomodoro for a task")
        print("4. Show tasks")
        print("5. Daily summary")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            name = input("Task name: ")
            category = input("Category: ")
            estimated = input("Estimated Pomodoros: ")
            add_task(name, category, estimated)
            print("Task added")

        elif choice == "2":
            timer.start()

        elif choice == "3":
            task_name = select_task()
            if task_name:
                timer.start()
                timer.complete()
                complete_pomodoro(task_name)
                print(f"Pomodoro for '{task_name}' completed and recorded")

        elif choice == "4":
            show_tasks()

        elif choice == "5":
            daily_summary()

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again")

if __name__ == "__main__":
    main()

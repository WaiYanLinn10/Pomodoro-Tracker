from timer import PomodoroTimer
from task import add_task, complete_pomodoro, read_tasks,show_tasks, select_task, check_task_status, pomodoros_count
from datetime import date

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
            due_date = input("Due date (YYYY-MM-DD): ")
            add_task(name, category, estimated, due_date)
            print("Task added")

        elif choice == "2":
            timer.start()

        elif choice == "3":
            task_name = select_task()
           
            if task_name:
                while True:
                    if check_task_status(task_name):
                        print(f"Task '{task_name}' is already completed.")
                        break

                    timer.start()
                    timer.complete()
                    complete_pomodoro(task_name)
                    print(f"Pomodoro for '{task_name}' completed and recorded")
            
                    study_again = input("Start another Pomodoro for this task? (y/n): ").lower()
                    if study_again != "y":
                        break

        elif choice == "4":
            show_tasks()

        elif choice == "5":
            today_pomodoros_count = pomodoros_count()         
            print(f"Pomodoros completed today: {today_pomodoros_count}")
            print(f"Focus time today: {today_pomodoros_count * 25} minutes")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice, try again")

if __name__ == "__main__":
    main()

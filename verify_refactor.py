import os
from datetime import date, timedelta
from task import TaskManager


def test_backend():
    print("Testing Backend Logic...")

    # Setup: Clean test files
    if os.path.exists("tasks.csv"):
        os.remove("tasks.csv")
    if os.path.exists("count_pomodoro.csv"):
        os.remove("count_pomodoro.csv")

    manager = TaskManager()


    # Add Task
    today = date.today().isoformat()
    success, msg = manager.add_task("Test Task", "Study", 2, today)
    assert success, f"Failed to add task: {msg}"
    print("✓ Task added successfully")

    # Duplicate Task
    success, msg = manager.add_task("Test Task", "Study", 3, today)
    assert not success, "Duplicate task should not be allowed"
    print("✓ Duplicate task prevented")

    # Due Date in the Past
    past_date = (date.today() - timedelta(days=1)).isoformat()
    success, msg = manager.add_task("Past Task", "Study", 1, past_date)
    assert not success, "Past due date should be rejected"
    print("✓ Past due date rejected")

    #  Invalid Date Format
    success, msg = manager.add_task("Bad Date Task", "Study", 1, "10/10/2026")
    assert not success, "Invalid date format should be rejected"
    print("✓ Invalid date format rejected")

    # Test Retrieval
    tasks = manager.get_all_tasks()
    assert len(tasks) == 1, "Should only have 1 valid task"
    task = tasks[0]
    assert task.name == "Test Task"
    assert task.status == "not started"
    print("✓ Task retrieval verified")

    # Pomodoro Logging
    success, msg = manager.log_pomodoro("Test Task")
    assert success, msg

    # Reload to test persistence
    new_manager = TaskManager()
    task = new_manager.get_task_by_name("Test Task")
    assert task.completed_pomodoros == 1
    assert task.status == "in progress"
    print("✓ Pomodoro logging verified")

    # Completion Logic
    new_manager.log_pomodoro("Test Task")  # 2/2
    task = new_manager.get_task_by_name("Test Task")
    assert task.completed_pomodoros == 2
    assert task.status == "completed"
    print("✓ Task completion verified")

    # Test Pomodoro for Invalid Task
    success, msg = new_manager.log_pomodoro("Unknown Task")
    assert not success, "Should not log pomodoro for non-existent task"
    print("✓ Pomodoro blocked for non-existent task")

    # Daily Pomodoro Count
    count = new_manager.get_todays_pomodoro_count()
    assert count == 2, f"Expected 2 pomodoros today, got {count}"
    print("✓ Daily pomodoro count verified")

    # Delete Task
    success, msg = new_manager.delete_task("Test Task")
    assert success, msg
    assert len(new_manager.get_all_tasks()) == 0
    print("✓ Task deletion verified")

    # Test Delete Non-existent Task
    success, msg = new_manager.delete_task("Ghost Task")
    assert not success, "Deleting non-existent task should fail"
    print("✓ Non-existent task delete handled correctly")

    print("\n ALL BACKEND TESTS PASSED!") 


if __name__ == "__main__":
    test_backend()

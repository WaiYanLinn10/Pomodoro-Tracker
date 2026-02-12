import os
from datetime import date, timedelta
from task import TaskManager


def test_backend():
    print("Testing Backend Logic...")

<<<<<<< HEAD
    # -----------------------------
    # 1. Setup: Clean test files
    # -----------------------------
=======
    # Setup: Clean test files
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    if os.path.exists("tasks.csv"):
        os.remove("tasks.csv")
    if os.path.exists("count_pomodoro.csv"):
        os.remove("count_pomodoro.csv")

    manager = TaskManager()

<<<<<<< HEAD
    # -----------------------------
    # 2. Test Add Task (VALID)
    # -----------------------------
=======

    # Add Task
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    today = date.today().isoformat()
    success, msg = manager.add_task("Test Task", "Study", 2, today)
    assert success, f"Failed to add task: {msg}"
    print("✓ Task added successfully")

<<<<<<< HEAD
    # -----------------------------
    # 3. Test Duplicate Task
    # -----------------------------
=======
    # Duplicate Task
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    success, msg = manager.add_task("Test Task", "Study", 3, today)
    assert not success, "Duplicate task should not be allowed"
    print("✓ Duplicate task prevented")

<<<<<<< HEAD
    # -----------------------------
    # 4. Test Due Date in the Past
    # -----------------------------
=======
    # Due Date in the Past
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    past_date = (date.today() - timedelta(days=1)).isoformat()
    success, msg = manager.add_task("Past Task", "Study", 1, past_date)
    assert not success, "Past due date should be rejected"
    print("✓ Past due date rejected")

<<<<<<< HEAD
    # -----------------------------
    # 5. Test Invalid Date Format
    # -----------------------------
=======
    #  Invalid Date Format
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    success, msg = manager.add_task("Bad Date Task", "Study", 1, "10/10/2026")
    assert not success, "Invalid date format should be rejected"
    print("✓ Invalid date format rejected")

<<<<<<< HEAD
    # -----------------------------
    # 6. Test Retrieval
    # -----------------------------
=======
    # Test Retrieval
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    tasks = manager.get_all_tasks()
    assert len(tasks) == 1, "Should only have 1 valid task"
    task = tasks[0]
    assert task.name == "Test Task"
    assert task.status == "not started"
    print("✓ Task retrieval verified")

<<<<<<< HEAD
    # -----------------------------
    # 7. Test Pomodoro Logging
    # -----------------------------
=======
    # Pomodoro Logging
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    success, msg = manager.log_pomodoro("Test Task")
    assert success, msg

    # Reload to test persistence
    new_manager = TaskManager()
    task = new_manager.get_task_by_name("Test Task")
    assert task.completed_pomodoros == 1
    assert task.status == "in progress"
    print("✓ Pomodoro logging verified")

<<<<<<< HEAD
    # -----------------------------
    # 8. Test Completion Logic
    # -----------------------------
=======
    # Completion Logic
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    new_manager.log_pomodoro("Test Task")  # 2/2
    task = new_manager.get_task_by_name("Test Task")
    assert task.completed_pomodoros == 2
    assert task.status == "completed"
    print("✓ Task completion verified")

<<<<<<< HEAD
    # -----------------------------
    # 9. Test Pomodoro for Invalid Task
    # -----------------------------
=======
    # Test Pomodoro for Invalid Task
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    success, msg = new_manager.log_pomodoro("Unknown Task")
    assert not success, "Should not log pomodoro for non-existent task"
    print("✓ Pomodoro blocked for non-existent task")

<<<<<<< HEAD
    # -----------------------------
    # 10. Test Daily Pomodoro Count
    # -----------------------------
=======
    # Daily Pomodoro Count
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    count = new_manager.get_todays_pomodoro_count()
    assert count == 2, f"Expected 2 pomodoros today, got {count}"
    print("✓ Daily pomodoro count verified")

<<<<<<< HEAD
    # -----------------------------
    # 11. Test Delete Task
    # -----------------------------
=======
    # Delete Task
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    success, msg = new_manager.delete_task("Test Task")
    assert success, msg
    assert len(new_manager.get_all_tasks()) == 0
    print("✓ Task deletion verified")

<<<<<<< HEAD
    # -----------------------------
    # 12. Test Delete Non-existent Task
    # -----------------------------
=======
    # Test Delete Non-existent Task
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082
    success, msg = new_manager.delete_task("Ghost Task")
    assert not success, "Deleting non-existent task should fail"
    print("✓ Non-existent task delete handled correctly")

<<<<<<< HEAD
    print("\n🎉 ALL BACKEND TESTS PASSED!")
=======
    print("\n ALL BACKEND TESTS PASSED!") 
>>>>>>> 183c680b90e65b6f2417286039eee298561f8082


if __name__ == "__main__":
    test_backend()

OOP Refactoring Guide: Pomodoro Tracker
This document provides a technical analysis of the current codebase for educational reference. It identifies specific violations of Object-Oriented Design principles and outlines the refactoring steps to correct them.

1. Analysis: Violations of OOP Principles
❌ Violation 1: Lack of Encapsulation
The Issue: The code uses raw dictionaries to represent Tasks.

# task.py
task = { "task_name": "Study", "status": "not started", ... }
Why this violates OOP: Encapsulation dictates that data (attributes) and methods (behavior) should be bundled together, and internal state should be protected.

No Data Integrity: Any part of the code can modify the dictionary incorrectly (e.g., setting status = "banana"). There are no "setter" methods to validate changes.
Exposed Implementation: The rest of the app knows exactly how the data is structured. If we change the structure, we break every function that touches it.
❌ Violation 2: Violation of Single Responsibility Principle (SRP)
The Issue: Functions like 
select_task()
 mix Business Logic with User Interface.

def select_task():
    tasks = read_tasks()       # <--- Data Access Logic
    print("\nSelect a task:")  # <--- Presentation Logic (UI)
    choice = input(...)        # <--- Input Handling (UI)
Why this violates OOP: The Single Responsibility Principle states a module/class should have only one reason to change.

This function has two reasons to change: if the business rule for selecting a task changes, OR if we decide to change the text output.
This "Tight Coupling" makes it impossible to reuse this logic in a GUI or Web App and makes automated testing impossible.
❌ Violation 3: Low Cohesion (Global State)
The Issue: Functions are scattered as global procedures and rely on global constants (Task_File). Why this violates OOP: Cohesion refers to how closely related the functions in a module are.

While 
task.py
 groups task functions, they don't share state in a structured way.
There is no clear instance of a "Manager" or "Repo". The Task_File path is a hardcoded dependency, making it hard to test with a different file (e.g., a test database) without hacking global variables.
2. The OOP Fix (Refactoring Plan)
✅ Solution 1: Introduce a Task Class
Addresses: Encapsulation We will convert dictionaries to a Class.

Attributes: self.name, self.status, etc.
Methods: mark_complete(), add_pomodoro().
Validation: The class ensures a task is never in an invalid state.
✅ Solution 2: Introduce a TaskManager Class
Addresses: Cohesion We will group the file handling and list management into a single class.

This class "owns" the data.
It provides a clean API: manager.add_task(), manager.get_tasks().
It removes Reliance on Global State by allowing the filename to be passed in 
init
.
✅ Solution 3: Decouple Interface from Logic
Addresses: SRP

The TaskManager will only return data (objects or lists).
main.py
 will handle printing and user input.
This separates the "View" (Console) from the "Model" (Task Logic).
3. Implementation Checklist
Phase 1: The Task Model
 Define Task Class
init
: Set private/protected attributes.
from_dict/to_dict: specific methods for persistence, keeping internal representation execution-independent.
Phase 2: The TaskManager Controller
 Define TaskManager Class
load_tasks(): Internal method to handle CSV reading.
add_task()
: Accepts arguments, creates a Task object, validates it, and saves.
get_active_tasks(): Filtering logic moved here.
Phase 3: Update Main Application
 Refactor 
main.py
Instantiate TaskManager.
Replace direct calls to 
task.py
 functions with manager method calls.
Crucial: Move all print statements out of 
task.py
 logic and into 
main.py
.
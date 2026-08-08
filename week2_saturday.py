# =============================================
# WEEK 2 · SATURDAY PROJECT
# Student Grade Tracker CLI
# =============================================
import json
import os

FILE = "grades.json"

# =============================================
# CLASS — Student
# =============================================
class Student:

    def __init__(self, name, grades=None):
        self.name   = name
        self.grades = grades if grades else []

    def add_grade(self, grade):
        if 0 <= grade <= 100:
            self.grades.append(grade)
            return True
        return False

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def highest(self):
        return max(self.grades) if self.grades else 0

    def lowest(self):
        return min(self.grades) if self.grades else 0

    def status(self):
        avg = self.average()
        if avg >= 80:
            return "Distinction"
        elif avg >= 60:
            return "Pass"
        elif avg >= 40:
            return "Borderline"
        else:
            return "Fail"

    def to_dict(self):
        return {
            "name"  : self.name,
            "grades": self.grades
        }

    def display(self, rank=None):
        prefix = f"{rank}. " if rank else "   "
        print(f"{prefix}{self.name:15} | "
              f"Avg: {self.average():5.1f} | "
              f"High: {self.highest():3} | "
              f"Low: {self.lowest():3} | "
              f"Status: {self.status()}")

# =============================================
# FILE OPERATIONS
# =============================================
def load_students():
    try:
        if not os.path.exists(FILE):
            return {}
        with open(FILE, "r") as f:
            data = json.load(f)
            return {
                name: Student(name, info["grades"])
                for name, info in data.items()
            }
    except json.JSONDecodeError:
        print("Warning: grades.json corrupted. Starting fresh.")
        return {}

def save_students(students):
    try:
        data = {name: s.to_dict() for name, s in students.items()}
        with open(FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving: {e}")

# =============================================
# MENU FUNCTIONS
# =============================================
def add_student(students):
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return
    if name in students:
        print(f"'{name}' already exists!")
        return
    students[name] = Student(name)
    save_students(students)
    print(f"Student '{name}' added!")

def add_grade(students):
    name = input("Student name: ").strip()
    if name not in students:
        print(f"'{name}' not found!")
        return
    try:
        grade = float(input("Enter grade (0-100): "))
        if students[name].add_grade(grade):
            save_students(students)
            print(f"Grade {grade} added for {name}!")
        else:
            print("Grade must be between 0 and 100!")
    except ValueError:
        print("Invalid grade — numbers only!")

def view_all(students):
    if not students:
        print("No students yet.")
        return

    # sort by average using lambda
    ranked = sorted(students.values(),
                    key=lambda s: s.average(),
                    reverse=True)

    print(f"\n{'='*65}")
    print(f"  {'STUDENT GRADE REPORT':^60}")
    print(f"{'='*65}")
    print(f"  {'Name':15} | {'Avg':>5} | {'High':>4} | "
          f"{'Low':>3} | Status")
    print(f"{'─'*65}")

    for i, student in enumerate(ranked):
        student.display(rank=i+1)

    print(f"{'─'*65}")

    # list comprehensions for stats
    averages      = [s.average() for s in students.values()]
    passing       = [s for s in students.values() if s.average() >= 60]
    failing       = [s for s in students.values() if s.average() < 60]
    distinctions  = [s for s in students.values() if s.average() >= 80]

    print(f"  Total students    : {len(students)}")
    print(f"  Class average     : {sum(averages)/len(averages):.1f}")
    print(f"  Passing           : {len(passing)}")
    print(f"  Failing           : {len(failing)}")
    print(f"  Distinctions      : {len(distinctions)}")
    print(f"{'='*65}\n")

def delete_student(students):
    name = input("Student name to delete: ").strip()
    if name not in students:
        print(f"'{name}' not found!")
        return
    confirm = input(f"Delete '{name}'? (y/n): ")
    if confirm.lower() == "y":
        del students[name]
        save_students(students)
        print(f"'{name}' deleted!")

def search_student(students):
    name = input("Search name: ").strip()
    if name not in students:
        print(f"'{name}' not found!")
        return
    s = students[name]
    print(f"\n{'='*40}")
    print(f"  Student: {s.name}")
    print(f"{'='*40}")
    print(f"  Grades  : {s.grades}")
    print(f"  Average : {s.average():.1f}")
    print(f"  Highest : {s.highest()}")
    print(f"  Lowest  : {s.lowest()}")
    print(f"  Status  : {s.status()}")
    print(f"{'='*40}\n")

# =============================================
# MAIN MENU
# =============================================
def show_menu():
    print("\n" + "="*35)
    print("   STUDENT GRADE TRACKER")
    print("="*35)
    print("1. Add student")
    print("2. Add grade")
    print("3. View all students")
    print("4. Search student")
    print("5. Delete student")
    print("0. Exit")
    print("="*35)

def main():
    students = load_students()
    print(f"Loaded {len(students)} students from file.")

    while True:
        show_menu()
        choice = input("Choose (0-5): ").strip()

        if choice == "0":
            print("Goodbye! Keep coding. 💪")
            break
        elif choice == "1":
            add_student(students)
        elif choice == "2":
            add_grade(students)
        elif choice == "3":
            view_all(students)
        elif choice == "4":
            search_student(students)
        elif choice == "5":
            delete_student(students)
        else:
            print("Invalid choice!")

main()
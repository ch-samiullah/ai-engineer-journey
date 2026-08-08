# =============================================
# WEEK 1 · DAY 1 — Variables & Data Types
# Samiullah's AI Engineer Journey
# =============================================

# --- STRINGS (text) ---
my_name = "Samiullah"
my_goal = "AI Automation Engineer"
my_city = "Rawalpindi"

print("My name is:", my_name)
print("My goal:", my_goal)
print("I am from:", my_city)

#  INTEGERS (whole numbers) 
my_age = 21
semester = 8
study_hours_weekday = 1
study_hours_weekend = 3

print("I am", my_age, "years old")
print("Currently in semester:", semester)

# --- FLOATS (decimal numbers) ---
current_cgpa = 2.8
target_cgpa = 3.5

print("Current CGPA:", current_cgpa)
print("Target CGPA:", target_cgpa)

# --- BOOLEANS (True or False) ---
is_employed = False
is_learning_python = True

print("Am I employed?", is_employed)
print("Am I learning Python?", is_learning_python)

# --- F-STRINGS (cleaner way to print) ---
print(f"\nMy name is {my_name} and I want to become an {my_goal}.")
print(f"I will study {study_hours_weekday} hour on weekdays and {study_hours_weekend} hours on weekends.")
print(f"I will raise my CGPA from {current_cgpa} to {target_cgpa}.")
print(f"I will raise my ",target_cgpa)
x = 'awesome'

def myfunc():
  x = "fantastic"
  print("Python is " + x)

myfunc()

print("Python is " + x)

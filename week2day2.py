# --- WRITE dict TO a .json file ---
student = {
    "name": "Samiullah",
    "age": 21,
    "cgpa": 2.8,
    "skills": ["Python", "Lists", "Loops", "Functions"],
    "goal": "AI Automation Engineer"
}

import json

with open("student.json", "w") as f:
    json.dump(student, f, indent=4)

print("JSON file saved!")

# --- READ from a .json file ---
with open("student.json", "r") as f:
    loaded = json.load(f)

print(type(loaded))           # <class 'dict'>
print(loaded["name"])         # Samiullah
print(loaded["skills"])       # ['Python', 'Lists'...]
print(loaded["skills"][0])    # Python

# --- UPDATE JSON file ---
loaded["cgpa"] = 3.0
loaded["skills"].append("Dictionaries")

with open("student.json", "w") as f:
    json.dump(loaded, f, indent=4)

print("JSON updated!")

# --- READ UPDATED FILE ---
with open("student.json", "r") as f:
    updated = json.load(f)
print(updated)
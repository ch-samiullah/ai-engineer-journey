class student:
    def __init__(self, age, name, cgpa=None):
        self.name = name
        self.age = age
        self.cgpa = cgpa
        self.skills = []

    # --- METHOD (function inside a class) ---
    def introduction(self):
        print(f"my name is {self.name} and i am {self.age} years old")

    def add_skills(self, skill):
        self.skills.append(skill)
        print(f"skill '{skill}' added")
        


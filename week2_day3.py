# --- CATCHING MULTIPLE ERRORS ---
def safe_disision(a,b):
    try:
        result=a/b
        return result
    except ZeroDivisionError:
        return"You can't divide by zero!"
    except TypeError:
        return"YOu can't divide by a string!"
    print("plz enter a number")
    print(safe_disision(10,2))
    print(safe_disision(10,6))
    # --- RAISING YOUR OWN ERRORS ---
    def check_cgpa(cgpa):
        if cgpa<2.0:
            raise ValueError("CGPA must be at least 2.0")
        else:
            return "CGPA is valid!"
    print(check_cgpa(3.5))  # CGPA is valid!
    # --- CATCHING ALL ERRORS (use carefully) ---
try:
    result = 10 / 6
except Exception as e:
    print(f"Something went wrong: {e}")
    print(f"Error type: {type(e).__name__}")
# =============================================
# MINI PROJECT — Bulletproof File Reader
# =============================================
import json
import os

def read_json_file(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return f"Error: '{filename}' not found."
    except json.JSONDecodeError:
        return f"Error: '{filename}' is not valid JSON."
    except PermissionError:
        return f"Error: No permission to read '{filename}'."

def get_valid_number(prompt, min_val, max_val):
    while True:
        try:
            num = float(input(prompt))
            if num < min_val or num > max_val:
                print(f"Enter a number between {min_val} and {max_val}")
                continue
            return num
        except ValueError:
            print("Invalid input. Numbers only!")

def safe_calculator():
    print("=" * 35)
    print("   BULLETPROOF CALCULATOR")
    print("=" * 35)

    while True:
        try:
            a = float(input("First number: "))
            b = float(input("Second number: "))
            op = input("Operation (+, -, *, /): ")

            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            elif op == "/":
                if b == 0:
                    raise ZeroDivisionError
                result = a / b
            else:
                raise ValueError(f"Unknown operation: {op}")

            print(f"Result: {a} {op} {b} = {result}")

        except ZeroDivisionError:
            print("Cannot divide by zero!")
        except ValueError as e:
            print(f"Invalid input: {e}")
        except KeyboardInterrupt:
            print("\nCalculator closed. Goodbye!")
            break

        again = input("Calculate again? (y/n): ")
        if again.lower() != "y":
            break

# --- RUN ---
print(read_json_file("contacts.json"))     # works
print(read_json_file("missing.json"))      # handled
print(read_json_file("week2_day2.py"))     # invalid JSON handled

cgpa = get_valid_number("Enter CGPA: ", 0, 4)
print(f"Your CGPA is: {cgpa}")

safe_calculator()
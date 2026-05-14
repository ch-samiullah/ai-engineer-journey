# =============================================
# WEEK 1 · DAY 5 — CLI Calculator
# =============================================

# --- STEP 1: Functions for each operation ---
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero!"
    return a / b

def power(a, b):
    return a ** b     # ** means "to the power of"

def modulus(a, b):
    return a % b      # % gives the remainder

# --- STEP 2: Display menu ---
def show_menu():
    print("\n--- CALCULATOR MENU ---")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power (a^b)")
    print("6. Modulus (remainder)")
    print("0. Exit")
    print("-" * 22)

# --- STEP 3: Main calculator logic ---
def calculator():
    print("=" * 30)
    print("   Samiullah's CLI Calculator")
    print("=" * 30)

    while True:
        show_menu()
        choice = input("Choose operation (0-6): ")

        if choice == "0":
            print("Goodbye! Keep coding.")
            break

        if choice not in ["1","2","3","4","5","6"]:
            print("Invalid choice. Try again.")
            continue   # skip to next loop iteration

        # Get numbers from user
        try:
            a = float(input("Enter first number: "))
            b = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter numbers only.")
            continue

        # Calculate based on choice
        if choice == "1":
            result = add(a, b)
            operation = "+"
        elif choice == "2":
            result = subtract(a, b)
            operation = "-"
        elif choice == "3":
            result = multiply(a, b)
            operation = "*"
        elif choice == "4":
            result = divide(a, b)
            operation = "/"
        elif choice == "5":
            result = power(a, b)
            operation = "^"
        elif choice == "6":
            result = modulus(a, b)
            operation = "%"

        print(f"\nResult: {a} {operation} {b} = {result}")

# --- STEP 4: Run it ---
calculator()
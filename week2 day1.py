with open("notes.txt", "w") as f:
    f.write("my name is sami\n")
    print("file written")

with open("notes.txt", "r") as f:
    content = f.read()
print(content)

with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())

with open("notes.txt", "r") as f:
    lines = f.readlines()
    print(lines)
    print(f"Total lines: {len(lines)}")

with open("notes.txt", "a") as f:
    f.write("week2\n")


# --- CHECK if file exists before reading ---
import os

if os.path.exists("notes.txt"):
    with open("notes.txt", "r") as f:
        print(f.read())
else:
    print("File not found!")

# --- DELETE a file ---
if os.path.exists("notes.txt"):
    os.remove("notes.txt")
    print("File deleted!")

# --- FILE INFO ---
with open("week2_day1.py", "r") as f:
    content = f.read()
    words = len(content.split())
    lines = len(content.splitlines())
    print(f"This file has {words} words and {lines} lines")

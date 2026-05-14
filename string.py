# =============================================
# WEEK 1 · SATURDAY — Strings Deep Dive
# =============================================

sentence = "  Hello, I am Samiullah and I want to become an AI Engineer  "

# --- CLEANING ---
print(sentence.strip())          # removes spaces from both ends
print(sentence.lower())          # all lowercase
print(sentence.upper())          # all uppercase
print(sentence.title())          # Every Word Capitalized

# --- SEARCHING ---
print(sentence.count("I"))       # how many times "I" appears
print(sentence.find("Samiullah")) # index position of word (-1 if not found)
print("AI" in sentence)          # True/False — does it contain "AI"?

# --- REPLACING ---
print(sentence.replace("AI Engineer", "AI Automation Engineer"))

# --- SPLITTING (string → list) ---
words = sentence.strip().split(" ")   # splits by space
print(words)
print(len(words))                      # word count

# --- JOINING (list → string) ---
word_list = ["Python", "is", "powerful"]
joined = " ".join(word_list)
print(joined)                # Python is powerful

csv_line = ",".join(word_list)
print(csv_line)              # Python,is,powerful

# --- SLICING (same as lists) ---
text = "Samiullah"
print(text[0:4])     # Sami
print(text[-4:])     # llah
print(text[::-1])    # halleimaS — reversed!

# --- CHECKING ---
print("hello123".isalpha())    # False — has numbers
print("hello".isalpha())       # True — only letters
print("123".isdigit())         # True — only numbers
print("  ".isspace())          # True — only spaces

# --- FORMATTING ---
name = "samiullah"
print(name.capitalize())       # Samiullah — first letter only
print(f"{'Name':>15}")         # right-aligned in 15 spaces
print(f"{'Name':<15}|")        # left-aligned in 15 spaces
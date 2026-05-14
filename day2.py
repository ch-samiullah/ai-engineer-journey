# =============================================
# WEEK 1 · DAY 2 — Lists & Loops
# =============================================

# --- CREATING LISTS ---
skills = ["Python", "LangChain", "Claude API", "n8n", "Prompt Engineering"]
numbers = [10, 25, 37, 42, 58]
mixed = ["Samiullah", 21, True, 3.5]   # lists can mix types

# --- ACCESSING ITEMS (indexing starts at 0) ---
print(skills[0])    # Python      → first item
print(skills[1])    # LangChain   → second item
print(skills[-1])   # Prompt Engineering → LAST item

# --- LIST LENGTH ---
print(len(skills))  # 5

# --- ADD an item ---
skills.append("FastAPI")
print(skills)       # now has 6 items

# --- REMOVE an item ---
skills.remove("FastAPI")
print(skills)       # back to 5

# --- CHANGE an item ---
skills[0] = "Python 3.11"
print(skills[0])    # Python 3.11

# --- SLICING (grab a portion) ---
print(skills[0:3])  # first 3 items
print(skills[2:])   # from index 2 to end
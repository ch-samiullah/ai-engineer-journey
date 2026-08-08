# =============================================
# WEEK 5 · SATURDAY — AI Personal Assistant
# Sab kuch combine: Chat + JSON + File saving
# =============================================

import os                              # environment variables ke liye
import json                            # JSON parse karne ke liye
from datetime import datetime          # 🆕 NEW CONCEPT — current date/time lene ke liye
from groq import Groq                  # Groq API
from dotenv import load_dotenv         # .env file padhne ke liye

load_dotenv()                          # .env pehle load karo
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ----------------------------------------
# 🆕 NEW CONCEPT — Constants
# Capital letters mein likhte hain — change nahi hote
# Pure program mein same rehte hain
# ----------------------------------------
MODEL = "llama-3.3-70b-versatile"     # ek jagah define — poora code use karega
HISTORY_FILE = "chat_history.json"    # history file ka naam
MAX_HISTORY = 20                       # maximum messages yaad rakhne ki limit

# ----------------------------------------
# PART 1 — File Operations
# Chat history save aur load karna
# ----------------------------------------

def save_history(history):
    # 🆕 NEW CONCEPT — json.dump()
    # Python dictionary/list ko JSON file mein likhna
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)   # indent=2 = readable format
    print(f"✅ History saved to {HISTORY_FILE}")

def load_history():
    # 🆕 NEW CONCEPT — os.path.exists()
    # check karo file exist karti hai ya nahi
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            # 🆕 NEW CONCEPT — json.load()
            # JSON file ko Python list mein convert karna
            return json.load(f)
    return []                              # file nahi hai toh empty list

# ----------------------------------------
# PART 2 — Core Chat Function
# ----------------------------------------

def chat(system_role, history, user_message):
    # messages list banao — system + history + naya message
    messages = [{"role": "system", "content": system_role}]
    messages.extend(history)               # poori history add karo
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,                       # upar define kiya tha
        temperature=0.7,
        messages=messages
    )

    ai_reply = response.choices[0].message.content

    # history update karo
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ai_reply})

    # history zyada bari ho jaaye toh purani hatao
    if len(history) > MAX_HISTORY:
        history = history[2:]

    return ai_reply, history

# ----------------------------------------
# PART 3 — JSON Extractor Feature
# ----------------------------------------

def extract_info_from_text(text):
    # 🆕 NEW CONCEPT — multi-line f-string prompt
    # complex prompt banane ka tarika
    prompt = f"""Extract key information from this text and return as JSON:

Text: {text}

Return ONLY valid JSON, no markdown, no backticks:
{{
    "main_topic": "...",
    "key_points": ["...", "..."],
    "action_items": ["...", "..."],
    "summary": "one line summary"
}}"""

    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,                     # JSON ke liye 0 — consistent output
        messages=[
            {
                "role": "system",
                "content": "You are a JSON extractor. Return ONLY valid JSON."
            },
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(clean)           # parse karo
    except json.JSONDecodeError:
        return {"error": "Could not parse JSON"}

# ----------------------------------------
# PART 4 — Job Analyzer Feature
# ----------------------------------------

def analyze_job(job_desc):
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a job analyzer. Return ONLY valid JSON."
            },
            {
                "role": "user",
                "content": f"""Analyze this job:

{job_desc}

Return ONLY valid JSON:
{{
    "title": "...",
    "skills": ["...", "..."],
    "experience": "...",
    "salary": "...",
    "remote": true/false,
    "fresh_grad_ok": true/false,
    "match_score": 0-100
}}"""
            }
        ]
    )

    raw = response.choices[0].message.content
    clean = raw.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(clean)
    except:
        return {"error": "Parse failed"}

# ----------------------------------------
# PART 5 — Display Functions
# ----------------------------------------

def show_menu():
    print("\n" + "="*45)
    print("   🤖 TARS — AI Personal Assistant")
    print("="*45)
    print("1. Chat with TARS")
    print("2. Extract info from text")
    print("3. Analyze a job description")
    print("4. View chat history")
    print("5. Save & Exit")
    print("="*45)

def display_json(data, title):
    # dictionary ko nicely print karo
    print(f"\n--- {title} ---")
    for key, value in data.items():        # har key-value pair print karo
        if isinstance(value, list):        # 🆕 isinstance() — check karo list hai ya nahi
            print(f"{key}:")
            for item in value:             # list items bullet ke saath
                print(f"  • {item}")
        else:
            print(f"{key}: {value}")

# ----------------------------------------
# MAIN PROGRAM — Sab Features Combine
# ----------------------------------------

def main():
    # system role — TARS ka character
    system_role = """You are TARS, an AI assistant for Samiullah —
a Pakistani CS graduate learning AI automation to get a job 
and move to Norway for Masters. You know Python, Groq API, 
n8n, LangChain. Be helpful, concise, and motivating."""

    # purani history load karo — agar file hai
    history = load_history()

    if history:
        print(f"✅ Loaded {len(history)} previous messages")

    while True:
        show_menu()
        choice = input("\nChoose (1-5): ").strip()

        # ----------------------------------------
        # OPTION 1 — Normal Chat
        # ----------------------------------------
        if choice == "1":
            print("\n💬 Chat Mode (type 'back' to return)\n")
            while True:
                user_input = input("You: ").strip()

                if user_input.lower() == "back":
                    break

                if not user_input:
                    continue

                # 🆕 NEW CONCEPT — datetime.now()
                # current time lena — log mein save ke liye
                timestamp = datetime.now().strftime("%H:%M")

                reply, history = chat(system_role, history, user_input)
                print(f"\n[{timestamp}] TARS: {reply}\n")

        # ----------------------------------------
        # OPTION 2 — Text Info Extractor
        # ----------------------------------------
        elif choice == "2":
            print("\n📝 Text Extractor (paste text, Enter twice when done)\n")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            if lines:
                text = " ".join(lines)
                print("\nExtracting info...")
                result = extract_info_from_text(text)
                display_json(result, "EXTRACTED INFO")

        # ----------------------------------------
        # OPTION 3 — Job Analyzer
        # ----------------------------------------
        elif choice == "3":
            print("\n💼 Job Analyzer (paste job description, Enter twice)\n")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)

            if lines:
                job = " ".join(lines)
                print("\nAnalyzing job...")
                result = analyze_job(job)
                display_json(result, "JOB ANALYSIS")

        # ----------------------------------------
        # OPTION 4 — View History
        # ----------------------------------------
        elif choice == "4":
            if not history:
                print("\nNo chat history yet.")
            else:
                print(f"\n--- CHAT HISTORY ({len(history)} messages) ---")
                for msg in history:
                    # role ke hisaab se prefix lagao
                    prefix = "You" if msg["role"] == "user" else "TARS"
                    # sirf pehle 100 characters dikhao — zyada lamba nahi
                    print(f"{prefix}: {msg['content'][:100]}...")

        # ----------------------------------------
        # OPTION 5 — Save aur Exit
        # ----------------------------------------
        elif choice == "5":
            save_history(history)          # file mein save karo
            print("Goodbye! Keep coding. 💪")
            break

        else:
            print("Invalid choice — 1 se 5 mein se choose karo")

# program shuru karo
main()
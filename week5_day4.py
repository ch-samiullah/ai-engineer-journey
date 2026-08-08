# =============================================
# WEEK 5 · DAY 4 — Structured Output + JSON
# Groq API use kar rahe hain — free & fast
# =============================================

import json
import os                    # JSON parse karne ke liye
from dotenv import load_dotenv
from flask.cli import load_dotenv
from groq import Groq          # Groq library import

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ----------------------------------------
# FUNCTION 1 — Basic JSON maangna AI se
# ----------------------------------------

def ask_json(prompt, schema):
    # Groq API ko call karo
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",        # free Groq model
        temperature=0,                  # 0 = consistent output, creative nahi
        messages=[
            {
                "role": "system",       # AI ko instructions dena
                # AI ko strictly JSON dene ko bol rahe hain
                "content": "You are a JSON generator. Return ONLY valid JSON. No explanation, no markdown, no backticks. Pure JSON only."
            },
            {
                "role": "user",         # user ka message
                # prompt + schema dono bhej rahe hain
                "content": f"{prompt}\n\nReturn JSON matching exactly this structure:\n{schema}"
            }
        ]
    )

    # AI ka raw response text nikaalo
    raw = response.choices[0].message.content

    # Backtick cleaning — agar model ne ```json``` add kiya ho
    clean = raw.replace("```json", "").replace("```", "").strip()

    # String ko Python dictionary mein convert karo
    return json.loads(clean)


# --- TEST 1: Simple info ---

# schema batao — AI exactly yeh structure follow karega
schema1 = '{"name": "...", "city": "...", "job": "...", "salary_pkr": 0}'

# function call karo
result = ask_json(
    prompt="Give me info about a Python developer named Ali from Lahore",
    schema=schema1
)

# results print karo
print("--- Test 1 Result ---")
print(result)                          # poora dictionary print
print(f"Name: {result['name']}")       # sirf naam
print(f"City: {result['city']}")       # sirf city
print(f"Salary: {result['salary_pkr']}")  # sirf salary
def ask_json_safe(prompt, schema):
    try:
        response= client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a JSON generator. Return ONLY valid JSON. No explanation, no markdown, no backticks. Pure JSON only."
                },
                {
                    "role": "user",
                    "content": f"{prompt}\n\nReturn JSON matching exactly this structure:\n{schema}"
                }

            ]
        )
        raw = response.choices[0].message.content
        clean = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)
        return{"success":True, "data":data}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"JSON parse failed: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    # --- TEST 2: Skills list ---
schema2 = '{"skills": [{"name": "...", "importance": "high/medium/low", "learn_days": 0}]}'

result2 = ask_json_safe(
    prompt="List 3 most important skills for an AI automation engineer",
    schema=schema2
)
if result2["success"]:
    print("\n--- AI Automation Skills ---")
    # list ke andar loop lagao
    for skill in result2["data"]["skills"]:
        # har skill ki info print karo
        print(f"• {skill['name']} — {skill['importance']} — {skill['learn_days']} days")
else:
    # error message print karo
    print(f"Error: {result2['error']}")
    # MINI PROJECT — Job Description Analyzer
  # ----------------------------------------
# MINI PROJECT — Job Description Analyzer
# ----------------------------------------

def analyze_job(job_description):
    # job analyzer ka schema — sab fields define kiye hain
    schema = '''{
    "job_title": "...",
    "required_skills": ["skill1", "skill2", "skill3"],
    "experience_years": 0,
    "salary_range": "...",
    "job_type": "remote/onsite/hybrid",
    "difficulty_level": "easy/medium/hard",
    "fresh_graduate_ok": true,
    "top_keywords": ["...", "...", "..."]
}'''

    # safe function call karo job description ke saath
    return ask_json_safe(
        prompt=f"Analyze this job description carefully:\n\n{job_description}",
        schema=schema
    )


def display_analysis(analysis):
    # pehle check karo success hua ya nahi
    if not analysis["success"]:
        print(f"Error: {analysis['error']}")
        return

    d = analysis["data"]               # data shortcut ke liye

    # formatted output print karo
    print("\n" + "="*45)
    print("       JOB ANALYSIS REPORT")
    print("="*45)
    print(f"Role          : {d['job_title']}")           # job title
    print(f"Type          : {d['job_type']}")             # remote/onsite
    print(f"Experience    : {d['experience_years']} yrs") # experience
    print(f"Salary        : {d['salary_range']}")         # salary
    print(f"Difficulty    : {d['difficulty_level']}")     # kitna hard
    # ternary operator — True/False ko Yes/No mein convert
    print(f"Fresh Grad?   : {'✅ Yes' if d['fresh_graduate_ok'] else '❌ No'}")

    # required skills list loop karo
    print(f"\nRequired Skills:")
    for skill in d['required_skills']:
        print(f"  • {skill}")          # har skill bullet ke saath

    # keywords list ko comma se join karo
    print(f"\nKeywords      : {', '.join(d['top_keywords'])}")
    print("="*45)


# ----------------------------------------
# MAIN PROGRAM — User se input lo
# ----------------------------------------

print("="*45)
print("   JOB DESCRIPTION ANALYZER")
print("   Powered by Groq + Llama3")
print("="*45)
print("Paste job description")
print("(Enter twice when done):\n")

lines = []                             # input lines store karne ke liye

while True:
    line = input()                     # ek line input lo
    if line == "":                     # empty line = done
        break
    lines.append(line)                 # line list mein add karo

job_text = " ".join(lines)            # sari lines ko ek string banao

if job_text:                           # agar kuch input diya
    print("\nAnalyzing with Groq...")  # user ko batao
    analysis = analyze_job(job_text)   # analyze karo
    display_analysis(analysis)         # results dikhao
else:
    print("No input given.")           # kuch nahi diya
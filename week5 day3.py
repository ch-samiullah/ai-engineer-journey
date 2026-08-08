# =============================================
# WEEK 5 · DAY 3 — Prompt Engineering
# AI se behtar jawab kaise nikalwao
# =============================================
import os                      # environment variables ke liye
from groq import Groq          # Groq AI library
from dotenv import load_dotenv # .env file load karne ke liye

load_dotenv()  # .env file se API key load karo

# Groq client banao — API key .env se uthao
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(prompt, system="You are a helpful assistant."):
    # AI ko call karo
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # free Groq model
        messages=[
            {"role": "system", "content": system},  # AI ka persona/role
            {"role": "user", "content": prompt}      # tumhara sawaal
        ]
    )
    return response.choices[0].message.content  # sirf text nikalo response se

# =============================================
# TECHNIQUE 1 — Zero Shot vs Few Shot
# =============================================
print("=" * 45)
print("TECHNIQUE 1 — Zero Shot vs Few Shot")
print("=" * 45)

# Zero Shot — koi example nahi diya, seedha poochha
zero_shot = ask("Classify this as positive or negative: 'I love Python!'")
print(f"Zero Shot: {zero_shot}")  # AI khud decide karta hai

# Few Shot — pehle examples diye taake AI samjhe pattern
few_shot = ask("""
Classify sentiment. Examples:
'I love this!' → Positive
'This is terrible!' → Negative
'It is okay' → Neutral

Now classify: 'Python is amazing for AI!'
""")
print(f"Few Shot: {few_shot}")  # examples ki wajah se better result

# =============================================
# TECHNIQUE 2 — Chain of Thought
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 2 — Chain of Thought")
print("=" * 45)

# Bina chain of thought — seedha jawab mangwaya
simple = ask("What is 15% of 847?")
print(f"Simple: {simple}")  # might be wrong

# Chain of thought — step by step sochne diya
# "Think step by step" likhne se AI galti kam karta hai
cot = ask("What is 15% of 847? Think step by step.")
print(f"Chain of Thought: {cot}")  # zyada accurate answer

# =============================================
# TECHNIQUE 3 — Role Prompting
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 3 — Role Prompting")
print("=" * 45)

# Normal — koi role nahi, generic jawab aata hai
normal = ask("How do I learn Python?")
print(f"Normal: {normal[:100]}...")  # sirf pehle 100 characters print karo

# Role diya — AI specific expert ban gaya
expert = ask(
    "How do I learn Python?",
    system="""You are a senior Python developer with 10 years experience.
    Give practical advice in exactly 3 bullet points. Be specific."""
    # system prompt mein role + format dono bataya
)
print(f"With Role: {expert}")  # specific aur practical jawab

# =============================================
# TECHNIQUE 4 — Output Format Control
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 4 — Output Format")
print("=" * 45)

# AI se JSON format mein jawab mangwaya
# taake baad mein Python mein parse kar sakein
json_response = ask("""
Extract information from this text and return as JSON only:
'Samiullah is a 21 year old CS student from Rawalpindi with CGPA 2.8'

Return exactly this format:
{
  "name": "",
  "age": 0,
  "city": "",
  "cgpa": 0.0
}
""")
print(f"JSON Output: {json_response}")  # structured data nikala text se

# =============================================
# TECHNIQUE 5 — Prompt Templates
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 5 — Prompt Templates")
print("=" * 45)

def summarize(text, max_words=50):
    # reusable template — variables inject karo f-string se
    prompt = f"""Summarize the following text in maximum {max_words} words.
    
Text: {text}

Summary:"""  # "Summary:" likh ke AI ko hint diya ke yahan se likhna hai
    return ask(prompt)

def analyze_code(code):
    # code analysis ke liye structured prompt
    prompt = f"""Analyze this Python code and tell me:
1. What it does       
2. Any bugs           
3. How to improve it  

Code:
````python
{code}
```"""  # code backticks mein diya taake AI samjhe yeh code hai
    return ask(prompt)

# summarizer test karo
sample_text = """Python is a high-level programming language known for its 
simplicity and readability. It is widely used in AI, web development, 
data science, and automation. Python has a large community and thousands 
of libraries available."""

print(f"Summary: {summarize(sample_text, 20)}")  # 20 words mein summary

# code analyzer test karo
sample_code = """
def calculate(nums):
    total = 0
    for n in nums:
        total = total + n
    return total/len(nums)  # bug: crash karega agar empty list ho
"""
print(f"\nCode Analysis: {analyze_code(sample_code)}")  # AI bugs dhundega

# =============================================
# CHALLENGE — Job Description Generator
# =============================================
def job_description_generator(job_title, skills_list, experience_years):
    # skills list ko string mein convert karo
    skills_str = ", ".join(skills_list)  # ["Python", "AI"] → "Python, AI"
    
    # role prompting + output format dono use kiye
    prompt = f"""Create a professional job description for:
Job Title: {job_title}
Required Skills: {skills_str}
Experience: {experience_years} years

Format:
- Job Summary (2 lines)
- Key Responsibilities (3 points)
- Requirements (3 points)"""

    return ask(
        prompt,
        system="You are an expert HR manager. Write clear, professional job descriptions."
        # HR manager role diya — professional output aayega
    )

# challenge test karo
print("\n" + "=" * 45)
print("CHALLENGE — Job Description Generator")
print("=" * 45)
print(job_description_generator(
    "AI Automation Engineer",           # job title
    ["Python", "Claude API", "n8n"],    # skills
    2  ))                                  # experience years



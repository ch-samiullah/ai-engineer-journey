# =============================================
# WEEK 5 · DAY 3 — Prompt Engineering
# AI se behtar jawab kaise nikalwao
# =============================================
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask(prompt, system="You are a helpful assistant."):
    # AI ko call karo aur jawab nikalo
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# =============================================
# TECHNIQUE 1 — Zero Shot vs Few Shot
# =============================================
print("=" * 45)
print("TECHNIQUE 1 — Zero Shot vs Few Shot")
print("=" * 45)

# Zero Shot — koi example nahi diya
zero_shot = ask("Classify this as positive or negative: 'I love Python!'")
print(f"Zero Shot: {zero_shot}")

# Few Shot — examples diye taake AI samjhe
few_shot = ask("""
Classify sentiment. Examples:
'I love this!' → Positive
'This is terrible!' → Negative
'It is okay' → Neutral

Now classify: 'Python is amazing for AI!'
""")
print(f"Few Shot: {few_shot}")

# =============================================
# TECHNIQUE 2 — Chain of Thought
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 2 — Chain of Thought")
print("=" * 45)

# Bina chain of thought
simple = ask("What is 15% of 847?")
print(f"Simple: {simple}")

# Chain of thought — step by step sochne dو
cot = ask("What is 15% of 847? Think step by step.")
print(f"Chain of Thought: {cot}")

# =============================================
# TECHNIQUE 3 — Role Prompting
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 3 — Role Prompting")
print("=" * 45)

# Normal jawab
normal = ask("How do I learn Python?")
print(f"Normal: {normal[:100]}...")

# Role diya — specific jawab aata hai
expert = ask(
    "How do I learn Python?",
    system="""You are a senior Python developer with 10 years experience.
    Give practical advice in exactly 3 bullet points. Be specific."""
)
print(f"With Role: {expert}")

# =============================================
# TECHNIQUE 4 — Output Format Control
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 4 — Output Format")
print("=" * 45)

# JSON format mein jawab mangwao
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
print(f"JSON Output: {json_response}")

# =============================================
# TECHNIQUE 5 — Prompt Template
# =============================================
print("\n" + "=" * 45)
print("TECHNIQUE 5 — Prompt Templates")
print("=" * 45)

def summarize(text, max_words=50):
    # template mein variable inject karo
    prompt = f"""Summarize the following text in maximum {max_words} words.
    
Text: {text}

Summary:"""
    return ask(prompt)

def analyze_code(code):
    prompt = f"""Analyze this Python code and tell me:
1. What it does
2. Any bugs
3. How to improve it

Code:
````python
{code}
```"""
    return ask(prompt)

# test summarizer
sample_text = """Python is a high-level programming language known for its 
simplicity and readability. It is widely used in AI, web development, 
data science, and automation. Python has a large community and thousands 
of libraries available."""

print(f"Summary: {summarize(sample_text, 20)}")

# test code analyzer
sample_code = """
def calculate(nums):
    total = 0
    for n in nums:
        total = total + n
    return total/len(nums)
"""
print(f"\nCode Analysis: {analyze_code(sample_code)}")


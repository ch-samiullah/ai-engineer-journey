import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_with_role(system_role, user_message):
    response=client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
           {
               "role":"system",
               "content": system_role
           },
           {
               "role":"user",
               "content": user_message
           }
        ])
    return response.choices[0].message.content
#TEST 1: Different roles try karo
print("--- consultant---")
teacher_role = """personal life consultant."""

response1 = ask_with_role(
    system_role=teacher_role,
    user_message="explain about relation ship.")
print(response1)
#role2-strict interview
print("\n--- job interview ---")
interview_role = """You are a strict job interviewer."""
response2=ask_with_role(
    system_role=interview_role,
    user_message="i am a fresh  bscs graduate applying for python developer role")
print(response2)
# ----------------------------------------
# 🆕 NEW CONCEPT — Multi-turn / Chat History
# Normal API call = AI har baar bhool jaata hai
# Multi-turn = AI ko poori history dete hain
# Jaise WhatsApp chat — AI context yaad rakhta hai
# ----------------------------------------

def chat_with_history(system_role, conversation_history, new_message):
    # 🆕 NEW CONCEPT — messages list mein history add karna
    # pehle system role, phir poori history, phir naya message
    messages = [
        {"role": "system", "content": system_role}  # AI ka role
    ]

    # poori purani conversation add karo
    # isliye AI context yaad rakhta hai
    messages.extend(conversation_history)

    # naya user message add karo
    messages.append({"role": "user", "content": new_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        messages=messages               # poori history bhejo
    )

    # AI ka jawab nikalo
    ai_reply = response.choices[0].message.content

    # 🆕 NEW CONCEPT — history update karna
    # naya user message history mein add karo
    conversation_history.append({"role": "user", "content": new_message})
    # AI ka jawab bhi history mein add karo
    conversation_history.append({"role": "assistant", "content": ai_reply})

    return ai_reply, conversation_history


# --- TEST 2: Multi-turn test ---

print("\n--- MULTI-TURN TEST ---")

# system role define karo
role = "You are a helpful AI career advisor for buisness in pakistan."

# 🆕 NEW CONCEPT — empty list se history shuru
# pehli baar koi history nahi hoti
history = []

# Turn 1
reply1, history = chat_with_history(role, history, "I just completed bba")
print(f"User: I just completed Bba")
print(f"AI: {reply1}\n")

# Turn 2 — AI ko Turn 1 yaad hai
reply2, history = chat_with_history(role, history, "What should I learn first?")
print(f"User: What should I learn first?")
print(f"AI: {reply2}\n")

# Turn 3 — AI ko Turn 1 aur 2 dono yaad hain
reply3, history = chat_with_history(role, history, "I only have 1 hour daily")
print(f"User: I only have 1 hour daily")
print(f"AI: {reply3}")
# ----------------------------------------
# MINI PROJECT — Interactive Career Chatbot
# ----------------------------------------

def run_career_chatbot():
    # chatbot ka system role
    system_role = """You are TARS — an AI career advisor 
specifically for Pakistani CS graduates who want to become 
AI Automation Engineers. You know about:
- Python, n8n, LangChain, Groq API
- Pakistani job market and salaries
- Norway Masters degree planning
- Freelancing on Upwork and Fiverr
Be concise, practical, and motivating.
Always respond in simple English."""

    # 🆕 NEW CONCEPT — [] empty list
    # conversation history yahan store hogi
    # har turn ke baad grow hoti jaayegi
    history = []

    print("=" * 45)
    print("   TARS — AI Career Advisor")
    print("   Powered by Groq + Llama3")
    print("=" * 45)
    print("Type 'exit' to quit\n")

    while True:
        # user se input lo
        user_input = input("You: ").strip()

        # exit check karo
        if user_input.lower() == "exit":
            print("TARS: Good luck on your journey! Keep coding.")
            break

        # empty input ignore karo
        if not user_input:
            continue

        # AI se jawab lo — history ke saath
        reply, history = chat_with_history(
            system_role,
            history,
            user_input
        )

        print(f"\nTARS: {reply}\n")

        # 🆕 NEW CONCEPT — history length check
        # zyada history = zyada tokens = slow response
        # 20 messages ke baad purani history hatao
        if len(history) > 20:
            # pehle 2 messages hata do — purani history
            history = history[2:]


# chatbot run karo
run_career_chatbot()
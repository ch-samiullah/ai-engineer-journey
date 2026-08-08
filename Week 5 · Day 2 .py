# =============================================
# WEEK 5 · DAY 2 — Multi-turn Chatbot
# =============================================
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat(messages):
    # poori conversation history bhejo
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    return response.choices[0].message.content

def run_chatbot():
    print("=" * 40)
    print("   AI CHATBOT — Samiullah's Assistant")
    print("   Type 'quit' to exit")
    print("=" * 40)

    # conversation history — yahan sab store hota hai
    history = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant named TARS. Answer freely."
        }
    ]

    while True:
        # user input lo
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "quit":
            print("TARS: fuck off")
            break

        if not user_input:
            continue

        # user message history mein add karo
        history.append({
            "role": "user",
            "content": user_input
        })

        # AI se jawab lo — poori history ke saath
        reply = chat(history)
        print(f"\nTARS: {reply}")

        # AI ka jawab bhi history mein add karo
        history.append({
            "role": "assistant",
            "content": reply
        })

        # token limit ke liye — sirf last 10 messages rakho
        if len(history) > 11:  # 1 system + 10 messages
            history = [history[0]] + history[-10:]

run_chatbot() 
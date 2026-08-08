# =============================================
# WEEK 7 DAY 1 — LangChain Fixed Version
# =============================================

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

# LLM setup — max_tokens nahi
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0.7
)

parser = StrOutputParser()

# ----------------------------------------
# PART 1 — Basic Call
# ----------------------------------------

messages = [
    SystemMessage(content="You are an expert AI automation engineer."),
    HumanMessage(content="What is LangChain in 3 simple lines?")
]

response = llm.invoke(messages)
print("--- Basic Response ---")
print(response.content)

# ----------------------------------------
# PART 2 — Chain
# ----------------------------------------

template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}. Be concise."),
    ("human", "Explain {topic} in 3 lines with one example.")
])

# chain banao
chain = template | llm | parser

result = chain.invoke({
    "domain": "AI automation",
    "topic": "LangChain chains"
})

print("\n--- Chain Result ---")
print(result)

# ----------------------------------------
# PART 3 — CV Analyzer
# ----------------------------------------

analyze_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict CV reviewer for tech companies."),
    ("human", """Analyze this profile:
{profile}

Return:
- Score: X/10
- Top 3 strengths
- Top 3 weaknesses
- Missing skills for Norway AI job""")
])

improve_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a career coach for AI engineers going to Norway."),
    ("human", """Based on this analysis:
{analysis}

Give 3 specific action items for THIS WEEK.""")
])

analyze_chain = analyze_prompt | llm | parser
improve_chain = improve_prompt | llm | parser

my_profile = """
Name: Samiullah
Degree: BSCS — FUUAST Islamabad — 2.8 CGPA
Skills: Python, n8n, Groq API, LangChain, Webhooks
Projects:
- Customer Review Analyzer
- Contact Form Handler
- AI Summarizer
- TARS Voice Assistant (incomplete)
Goal: AI Automation Engineer — Norway
"""

print("\n--- CV Analysis ---")
analysis = analyze_chain.invoke({"profile": my_profile})
print(analysis)

print("\n--- Action Items ---")
improvements = improve_chain.invoke({"analysis": analysis})
print(improvements)

# ----------------------------------------
# PART 4 — Memory — New Way
# ----------------------------------------

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# memory store
store = {}

def get_session_history(session_id: str):
    # 🆕 session ID se history lo ya banao
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# memory ke saath chain
memory_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful career advisor for Pakistani developers."),
    ("placeholder", "{history}"),
    ("human", "{input}")
])

memory_chain = memory_prompt | llm | parser

# 🆕 RunnableWithMessageHistory — chain ko memory deta hai
with_memory = RunnableWithMessageHistory(
    memory_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

# session config
config = {"configurable": {"session_id": "samiullah_session"}}

print("\n--- Memory Chat ---")

r1 = with_memory.invoke(
    {"input": "I am Samiullah, learning AI automation for Norway"},
    config=config
)
print(f"Turn 1: {r1}\n")

r2 = with_memory.invoke(
    {"input": "What should I focus on this week?"},
    config=config
)
print(f"Turn 2: {r2}\n")

r3 = with_memory.invoke(
    {"input": "Do you remember my name and goal?"},
    config=config
)
print(f"Turn 3: {r3}")
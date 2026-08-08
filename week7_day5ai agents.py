# =============================================
# WEEK 7 · DAY 5 — AI Agent
# Problem: Manual job hunting bohot time leta hai
# Solution: Agent jo khud search, match, recommend kare
# =============================================

import os
from datetime import datetime
from dotenv import load_dotenv

# langchain_groq — Groq API ko LangChain ke saath use karne ke liye
from langchain_groq import ChatGroq

# PromptTemplate — Agent ko ReAct format mein instructions dene ke liye
from langchain_core.prompts import PromptTemplate

# @tool — normal function ko agent tool banata hai
from langchain_core.tools import tool

# langchain_classic — create_react_agent aur AgentExecutor yahan hain
# langchain 1.x mein yeh langchain.agents se remove ho gaye
from langchain_classic.agents import create_react_agent, AgentExecutor

# DuckDuckGoSearchRun — free web search, koi API key nahi chahiye
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()

# temperature=0 — agent consistent logical decisions le
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ----------------------------------------
# TOOLS
# ----------------------------------------

# search_engine pehle initialize karo — web_search tool iske baad aaye
# warna NameError aayega — search_engine defined nahi hoga
search_engine = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search internet for current jobs, salaries, companies.
    Use for: job listings, company info, market research.
    Input: search query string"""
    return search_engine.run(query)

@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expressions accurately.
    Use for: salary calculations, savings, loan repayment.
    Input: math expression like '20 * 175 * 4'"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def get_profile(query: str) -> str:
    """Get Samiullah's complete profile, skills, projects.
    Use when: matching jobs to his background.
    Use when: checking what roles suit him."""
    return """
    Name: Samiullah
    Education: BSCS — FUUAST Islamabad — 2.8 CGPA

    Technical Skills:
    - Python (functions, OOP, APIs, file handling)
    - n8n workflow automation
    - LangChain + RAG systems
    - Groq API + LLM integration
    - Webhooks + REST APIs
    - Git + GitHub
    - ChromaDB vector database

    Projects Built:
    - Customer Review Analyzer (n8n + AI)
    - Contact Form Handler (Webhook + AI)
    - AI Summarizer (n8n + Groq)
    - TARS Voice Assistant (Python + ElevenLabs)
    - PDF RAG System (LangChain + ChromaDB)

    Status: Fresh graduate — self taught AI automation
    Location: Islamabad, Pakistan
    Goal: AI Automation Engineer — Norway later
    """

@tool
def get_date(query: str) -> str:
    """Get current date and time.
    Use when: user asks about today, current date."""
    return datetime.now().strftime("Date: %A %B %d %Y | Time: %I:%M %p")

tools = [web_search, calculate, get_profile, get_date]

# ----------------------------------------
# REACT PROMPT
# ----------------------------------------

# tool_names — yahan {tool_names} hoga, {tool_name} nahi
# Yeh ek common bug tha teri file mein
prompt = PromptTemplate.from_template("""
You are TARS — AI career assistant for Samiullah.
Help him find jobs and plan his career.

Available tools:
{tools}

Tool names: {tool_names}

ALWAYS use this exact format:
Thought: what should I do?
Action: tool_name
Action Input: input string
Observation: tool result

When you have final answer:
Thought: I have enough information
Final Answer: your complete answer

Question: {input}
{agent_scratchpad}
""")

# ----------------------------------------
# AGENT
# ----------------------------------------

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# max_iterations — yahan underscore hai, max_iteration nahi
# handle_parsing_errors — plural, handle_parsing_error nahi
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# ----------------------------------------
# JOB HUNTING TASKS
# ----------------------------------------

print("="*50)
print("   TARS — JOB HUNTER AGENT")
print("="*50)

print("\n🔍 Searching Python/AI jobs in Islamabad...")
r1 = executor.invoke({
    "input": "Find Python or AI automation jobs in Islamabad Pakistan. What companies are hiring right now?"
})
print(f"\n✅ {r1['output']}")

print("\n💰 Researching salaries...")
r2 = executor.invoke({
    "input": "What is average salary for fresh Python developer in Islamabad? Calculate monthly and yearly total."
})
print(f"\n✅ {r2['output']}")

print("\n🎯 Matching profile to jobs...")
r3 = executor.invoke({
    "input": "Based on Samiullah's profile and skills, what jobs suit him best in Pakistan right now?"
})
print(f"\n✅ {r3['output']}")

print("\n" + "="*50)
print("   ASK TARS ANYTHING")
print("   type 'exit' to quit")
print("="*50)

while True:
    q = input("\n❓ ").strip()
    if q.lower() == "exit":
        break
    if not q:
        continue
    r = executor.invoke({"input": q})
    print(f"\n🤖 TARS: {r['output']}")
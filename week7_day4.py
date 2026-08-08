# =============================================
# WEEK 7 · DAY 4 — AI Agents
# =============================================
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import  tool, Tool
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from datetime import datetime

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

# ----------------------------------------
# TOOLS — Agent ke paas kya powers hain
# ----------------------------------------

# 🆕 NEW CONCEPT — Tools
# Agent akela kuch nahi kar sakta
# Tools use karta hai — jaise human hands use karta hai
# Har tool = ek specific capability

# Tool 1 — Web Search
# DuckDuckGo isliye — free hai, no API key
search = DuckDuckGoSearchRun()

search_tool = Tool(
    name="web_search",
    # description bohot important hai
    # Agent yeh padhke decide karta hai
    # kab yeh tool use karna hai
    description="""Use this to search current information 
    from the internet. Input should be a search query.
    Use for: current news, prices, facts, recent events""",
    func=search.run
)

# Tool 2 — Calculator
# Agent math galat karta hai kabhi kabhi
# Calculator tool = accurate math
def calculate(expression: str) -> str:
    """Calculate mathematical expressions"""
    try:
        # eval isliye — math expression evaluate karna
        # sirf numbers aur operators allow karo
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Invalid calculation"

calc_tool = Tool(
    name="calculator",
    description="""Use for mathematical calculations.
    Input: math expression like '45 * 12' or '100 / 4'
    Use for: any math, currency conversion, percentages""",
    func=calculate
)

# Tool 3 — Current Date/Time
def get_datetime(query: str) -> str:
    """Get current date and time"""
    now = datetime.now()
    return f"Current date: {now.strftime('%A, %B %d, %Y')} Time: {now.strftime('%I:%M %p')}"

datetime_tool = Tool(
    name="get_datetime",
    description="""Use to get current date and time.
    Input: any string like 'now' or 'current'
    Use when: user asks about date, time, or 'today'""",
    func=get_datetime
)

# Tool 4 — Samiullah Ka Profile
def get_profile(query: str) -> str:
    """Get Samiullah's profile information"""
    profile = """
    Name: Samiullah
    Education: BSCS — FUUAST Islamabad — 2.8 CGPA
    Skills: Python, n8n, LangChain, Groq API, RAG, Webhooks
    Projects: Customer Review Analyzer, Contact Form Handler,
              AI Summarizer, TARS Voice Assistant, AutoNotes Pro
    Goal: AI Automation Engineer in Norway
    Timeline: OsloMet apply 2027, start September 2027
    Current: Week 7 of AI engineering roadmap
    """
    return profile

profile_tool = Tool(
    name="get_profile",
    description="""Get information about Samiullah's 
    background, skills, projects, and Norway plan.
    Use when asked about Samiullah specifically.""",
    func=get_profile
)

# All tools list
tools = [search_tool, calc_tool, datetime_tool, profile_tool]

# ----------------------------------------
# REACT AGENT PROMPT
# ----------------------------------------

# 🆕 NEW CONCEPT — ReAct
# Reason + Act = ReAct
# Agent pehle sochta hai (Reason)
# Phir karta hai (Act)
# Phir result dekhta hai
# Phir dobara sochta hai
# Jab tak answer na mile

react_prompt = PromptTemplate.from_template("""
You are TARS, a helpful AI assistant with access to tools.

Available tools:
{tools}

Tool names: {tool_names}

To use a tool, use this EXACT format:
Thought: What should I do?
Action: tool_name
Action Input: input for the tool
Observation: tool result

When you have the final answer:
Thought: I now have the answer
Final Answer: your answer here

Question: {input}

{agent_scratchpad}
""")

# ----------------------------------------
# AGENT BANAO
# ----------------------------------------

# 🆕 create_react_agent
# LLM + Tools + Prompt = Agent
# Agent khud decide karta hai kaunsa tool use karna
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt
)

# 🆕 AgentExecutor
# Agent ko run karne wala engine
# verbose=True → agent ki thinking dikhao
# max_iterations → infinite loop se bachao
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,          # agent ki thinking print karo
    max_iterations=5,      # max 5 steps
    handle_parsing_errors=True
)

# ----------------------------------------
# TEST KARO
# ----------------------------------------

print("="*50)
print("   TARS AI AGENT")
print("   Powered by ReAct + Groq")
print("="*50)

# Test 1 — Simple
print("\n--- Test 1: Date ---")
r1 = executor.invoke({
    "input": "What is today's date?"
})
print(f"Answer: {r1['output']}")

# Test 2 — Math
print("\n--- Test 2: Calculator ---")
r2 = executor.invoke({
    "input": "If I work 20 hours per week at 175 NOK per hour, how much will I earn in 4 weeks?"
})
print(f"Answer: {r2['output']}")

# Test 3 — Profile
print("\n--- Test 3: Profile ---")
r3 = executor.invoke({
    "input": "What are Samiullah's main skills and projects?"
})
print(f"Answer: {r3['output']}")

# Test 4 — Web Search
print("\n--- Test 4: Web Search ---")
r4 = executor.invoke({
    "input": "What is the current minimum wage in Norway 2025?"
})
print(f"Answer: {r4['output']}")

# Interactive Mode
print("\n" + "="*50)
print("   INTERACTIVE AGENT MODE")
print("   type 'exit' to quit")
print("="*50)

while True:
    q = input("\n❓ Ask TARS: ").strip()
    if q.lower() == "exit":
        break
    if not q:
        continue
    
    result = executor.invoke({"input": q})
    print(f"\n🤖 TARS: {result['output']}")



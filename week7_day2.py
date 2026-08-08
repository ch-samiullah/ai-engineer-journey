import os
from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
load_dotenv()
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
      model="llama-3.3-70b-versatile",  
    temperature=0
)
parser= StrOutputParser
#step1- Documents bnao
documents=[
    Document( 
        page_content=""" Samiullah is a BSCS graduate from FUUAST Islamabad with 2.8 CGPA.
        He is learning AI automation engineering.
        he lives in islamabad pakistan and wants to move to Norway for higher studies.
        His skills include Python, n8n, Groq API, LangChain, Webhooks, REST APIs.
        He wants to move to Norway for Masters in Industrial IT and Automation at OsloMet.
        He has an uncle in Oslo who can help with job search.
        """,
        metadata={"source":"profile","topic":"background"
                  }
    ),
    Document(
        page_content="""
        Samiullah's projects:
        1. Customer Review Analyzer — n8n + Groq AI — analyzes sentiment and generates replies
        2. Contact Form Handler — Webhook + AI — categorizes and prioritizes messages
        3. AI Summarizer — n8n + Groq — summarizes any text automatically
        4. TARS Voice Assistant — Python + ElevenLabs — in progress
        5. AutoNotes Pro — FYP project — AI powered note generator
        """,
        metadata={"source":"profile","topic":"projects"}
    ),
    Document(
        page_content="""
         Samiullah's Norway plan:
        - University: OsloMet — ACIT program
        - Timeline: Apply early 2027, start September 2027
        - Funding: 45 lac family loan — interest free
        - Uncle in Oslo — job help + financial guarantee
        - Part time work: 20 hours per week allowed
        - Summer full time work to repay loan
        - Loan repayment: 2.5 to 3 years
        """,
        metadata={"source":"norway_plan","topic":"goal"}
    )   ,
  Document(
        page_content="""
        Samiullah's learning roadmap:
        - Week 1-4: Python fundamentals — Done
        - Week 5: Groq API integration — Done
        - Week 6: n8n automation — Done
        - Week 7: LangChain + RAG — In progress
        - Week 8: AI Agents
        - Week 9: AutoNotes Pro complete
        - Week 10: FastAPI basics
        - Goal: Industry ready by October 2026
        """,
        metadata={"source": "roadmap", "topic": "learning"}
    )   
]
print(f"--- Documents Created ---")
from langchain_community.embeddings import HuggingFaceEmbeddings
...
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)
print("Embedding model loaded")
from langchain_community.vectorstores import Chroma
print("--- Creating Vector Store ---")
vectorstore= Chroma.from_documents(
    documents=documents,
    embedding=embeddings,

)
print("Vector store created")
#retriving
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
print("Retriever created")
#rag chain
reg_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a helpful assistant.
Answer questions using ONLY the provided context.
If answer is not in context, say 'I don't have that information'.
Context: {context}""",
    ),
    ("human", "{question}"),
])
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# RAG Chain:
# Question → retriever → context nikalo
# Question + context → prompt → llm → parser
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | reg_prompt
    | llm
    | StrOutputParser()
)
print("\n" + "="*50)
print("   RAG Q&A SYSTEM — SAMIULLAH")
print("="*50)
questions = [
    "What are Samiullah's main projects?",
    "What is Samiullah's Norway plan?",
    "What skills does Samiullah have?",
    "When will samiullah live in pakistan?",
    "What is Samiullah's CGPA?"   # test — kya context mein hai?
]

for q in questions:
    print(f"\n❓ {q}")
    answer = rag_chain.invoke(q)
    print(f"💬 {answer}")
    print("-" * 40)
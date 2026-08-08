from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Lightweight fallback LLM runnable so the chain stays defined in this example.
llm = RunnableLambda(lambda prompt: f"Analysis result for prompt: {prompt}")
parser = StrOutputParser()

profile_docs = [
    Document(page_content="""
    Technical Skills: Python, n8n, LangChain, Groq API, 
    REST APIs, Webhooks, JSON, Git, GitHub, ChromaDB,
    Prompt Engineering, RAG systems, Automation workflows
    """),
    Document(page_content="""
    Soft Skills: Fast learner, self motivated, English fluent,
    problem solver, works independently, remote work ready
    """),
    Document(page_content="""
    Experience: Fresh graduate, 7 weeks intensive AI training,
    6 real projects built, active GitHub portfolio,
    self taught automation engineer
    """)
]

# Vector store banao
emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vs = Chroma.from_documents(profile_docs, emb)
ret = vs.as_retriever(search_kwargs={"k": 3})

# JD Analyzer prompt
jd_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a job application advisor.
Given the candidate profile and job description,
analyze the fit.

Candidate Profile: {context}"""),
    ("human", """Job Description: {jd}

Analyze:
1. Match percentage (0-100%)
2. Matching skills
3. Missing skills
4. Should apply? Yes/No
5. One line advice""")
])

# JD chain
jd_chain = (
    {
        "context": ret | format_docs,
        "jd": RunnablePassthrough()
    }
    | jd_prompt
    | llm
    | parser
)

# Test karo
job1 = """
Python Developer needed. Must know REST APIs, 
automation tools, AI integration. n8n experience 
preferred. Fresh graduates welcome. Remote position.
"""

job2 = """
Senior DevOps Engineer. 5+ years Docker, Kubernetes,
AWS, Terraform. CI/CD pipeline expert required.
No fresh graduates.
"""

print("\n" + "="*50)
print("   JOB FIT ANALYZER")
print("="*50)

print("\n📋 Job 1 — Python Developer:")
print(jd_chain.invoke(job1))

print("\n📋 Job 2 — Senior DevOps:")
print(jd_chain.invoke(job2))

# =============================================
# WEEK 7 · DAY 3 — Real PDF RAG System
# =============================================

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 🆕 PyPDFLoader — PDF se text nikalne ke liye
# PDF binary format mein hoti hai
# Yeh loader pages extract karta hai readable text mein
from langchain_community.document_loaders import PyPDFLoader

# 🆕 RecursiveCharacterTextSplitter
# Pages bohot lambe hote hain — LLM context mein nahi aate
# Yeh splitter intelligently chunks banata hai
# "Recursive" isliye — pehle paragraphs, phir sentences,
# phir words — smartly split karta hai
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0
)

parser = StrOutputParser()

# ----------------------------------------
# STEP 1 — PDF Load + Split
# ----------------------------------------

def load_and_split(pdf_path):
    print(f"\n📄 Loading: {pdf_path}")
    
    # PDF load karo
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    print(f"✅ {len(pages)} pages loaded")
    
    # 🆕 chunk_size=500 — har chunk max 500 chars
    # chunk_overlap=50 — 50 chars overlap
    # Overlap isliye — agar important sentence
    # chunk boundary pe ho toh dono chunks mein rahe
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunks = splitter.split_documents(pages)
    print(f"✅ {len(chunks)} chunks created")
    
    return chunks

# ----------------------------------------
# STEP 2 — Vector Store
# ----------------------------------------

def create_vectorstore(chunks):
    print("\n⏳ Creating vector store...")
    
    # Free local embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Chunks → embed → store
    vs = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    
    print("✅ Vector store ready")
    return vs

# ----------------------------------------
# STEP 3 — RAG Chain
# ----------------------------------------

def create_rag_chain(vectorstore):
    
    # k=3 — top 3 relevant chunks
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
    
    def format_docs(docs):
        # Page number include karo
        # Isliye ke user ko pata chale
        # answer kahan se aaya
        result = []
        for doc in docs:
            page = doc.metadata.get('page', 0) + 1
            result.append(
                f"[Page {page}]\n{doc.page_content}"
            )
        return "\n\n".join(result)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a document assistant.
Answer using ONLY the provided context.
Always mention page number.
If not found say: 'Not found in document'

Context:
{context}"""),
        ("human", "{question}")
    ])
    
    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | parser
    )
    
    return chain

# ----------------------------------------
# STEP 4 — Interactive Q&A
# ----------------------------------------

def run_pdf_qa(pdf_path):
    
    # Load karo
    chunks = load_and_split(pdf_path)
    
    # Vector store banao
    vs = create_vectorstore(chunks)
    
    # Chain banao
    chain = create_rag_chain(vs)
    
    print("\n" + "="*50)
    print("   PDF Q&A READY")
    print(f"   File: {pdf_path}")
    print("   Type 'exit' to quit")
    print("="*50)
    
    while True:
        q = input("\n❓ Your question: ").strip()
        
        if q.lower() == "exit":
            print("Goodbye!")
            break
            
        if not q:
            continue
        
        print("🔍 Searching...")
        answer = chain.invoke(q)
        print(f"\n💬 Answer:\n{answer}")
        print("-"*40)

# ----------------------------------------
# MAIN
# ----------------------------------------

# PDF path — same folder mein rakho
PDF_PATH = "profile.pdf"

# File exist karta hai check karo
if os.path.exists(PDF_PATH):
    run_pdf_qa(PDF_PATH)
else:
    print(f"❌ File not found: {PDF_PATH}")
    print("profile.pdf same folder mein rakho!")
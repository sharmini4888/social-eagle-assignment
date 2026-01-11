from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

# 🔑 Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

import shutil

# 1. Clear existing vector DB if exists
if os.path.exists("chroma_db"):
    shutil.rmtree("chroma_db")
    print("🧹 Cleared existing vector database")

# 2. Load PDF
print("📄 Loading PDF...")
loader = PyPDFLoader("science.pdf")
documents = loader.load()
print(f"   Found {len(documents)} pages")

# 3. Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Increased chunk size for better context
    chunk_overlap=100
)
chunks = text_splitter.split_documents(documents)
print(f"   Split into {len(chunks)} chunks")

# 4. Create embeddings (OPENAI USED HERE 👇)
print("🧠 Creating embeddings and storing in Vector DB...")
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# 5. Store in Vector DB (Chroma)
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

# vector_db.persist() # Not needed in newer versions, but harmless

print("✅ PDF stored in Vector Database successfully!")


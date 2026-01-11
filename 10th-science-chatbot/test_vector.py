from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

docs = db.similarity_search("acid base", k=2)
for d in docs:
    print(d.page_content[:200])

from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# 🔑 OpenAI Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Vector DB
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# Neo4j
driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "knowledge_graph_demo_2024")
)

@app.get("/vector_search")
def vector_search(query: str):
    docs = vector_db.similarity_search(query, k=3)
    return {"results": [d.page_content for d in docs]}

@app.get("/kg_search")
def kg_search():
    with driver.session() as session:
        result = session.run("MATCH (c:Concept) RETURN c.name LIMIT 10")
        return {"concepts": [r["c.name"] for r in result]}

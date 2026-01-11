# ==========================================================
# HYBRID RAG: VECTOR (CHROMA) + KNOWLEDGE GRAPH (NEO4J)
# ==========================================================

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma

from neo4j import GraphDatabase
import spacy
import os

# -------- CONFIG --------
PDF_PATH = "data/sample.pdf"

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password"  # change this

# -------- LOAD NLP --------
nlp = spacy.load("en_core_web_sm")

# -------- 1. LOAD PDF --------
print("📄 Loading PDF...")
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()
print(f"✅ Loaded {len(documents)} pages")

# -------- 2. SPLIT TEXT --------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(documents)
print(f"✂️ Created {len(chunks)} chunks")

# -------- 3. VECTOR STORE (CHROMA) --------
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
vectorstore.persist()
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

print("📦 Vector DB ready")

# -------- 4. NEO4J CONNECTION --------
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def create_entity(tx, name, label):
    tx.run(
        f"MERGE (n:{label} {{name: $name}})",
        name=name
    )

def create_relation(tx, e1, e2):
    tx.run(
        """
        MATCH (a {name: $e1})
        MATCH (b {name: $e2})
        MERGE (a)-[:RELATED_TO]->(b)
        """,
        e1=e1,
        e2=e2
    )

# -------- 5. BUILD KNOWLEDGE GRAPH --------
print("🧠 Building Knowledge Graph...")

with driver.session() as session:
    for chunk in chunks:
        doc = nlp(chunk.page_content)
        entities = [ent.text for ent in doc.ents if ent.label_ in ["PERSON", "ORG", "GPE", "EVENT"]]

        # Create nodes
        for ent in entities:
            session.execute_write(create_entity, ent, "Entity")

        # Create relationships
        for i in range(len(entities) - 1):
            session.execute_write(create_relation, entities[i], entities[i + 1])

print("✅ Knowledge Graph created")

# -------- 6. LLM --------
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# -------- 7. CHAT LOOP (HYBRID) --------
print("\n🤖 Hybrid RAG Ready (Vector + KG)")
print("Ask questions or type 'exit'\n")

while True:
    query = input("You: ")
    if query.lower() == "exit":
        break

    # Vector context
    docs = retriever.invoke(query)
    vector_context = "\n".join(d.page_content for d in docs)

    prompt = f"""
You are an intelligent assistant.
Use the context below to answer.

Context:
{vector_context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)
    print("Bot:", response.content)

driver.close()

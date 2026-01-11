import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Neo4j connection
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "knowledge_graph_demo_2024")

app = Flask(__name__)
CORS(app)

class Neo4jHandler:
    def __init__(self):
        print("Initializing Knowledge Graph Connection...")
        try:
            self.driver = GraphDatabase.driver(
                NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
            )
            self.verify_connection()
            self.node_label = self.detect_node_label()
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            self.driver = None
            self.node_label = None

    def verify_connection(self):
        with self.driver.session() as session:
            session.run("RETURN 1")
            print("✅ Connected to Neo4j successfully.")

    def detect_node_label(self):
        with self.driver.session() as session:
            # Check for Concept
            result = session.run("MATCH (n:Concept) RETURN count(n) as count")
            if result.single()["count"] > 0:
                print("ℹ️ Detected 'Concept' nodes.")
                return "Concept"
            # Check for Entity
            result = session.run("MATCH (n:Entity) RETURN count(n) as count")
            if result.single()["count"] > 0:
                print("ℹ️ Detected 'Entity' nodes.")
                return "Entity"
            return None

    def search(self, query):
        if not self.driver or not self.node_label:
            return []
        
        # Simple keyword search on 'name'
        cypher = f"""
        MATCH (n:{self.node_label})
        WHERE toLower(n.name) CONTAINS toLower($search_term) 
           OR toLower(n.definition) CONTAINS toLower($search_term)
        RETURN n.name as name, n.definition as definition
        LIMIT 5
        """
        
        with self.driver.session() as session:
            result = session.run(cypher, search_term=query)
            return [f"{r['name']}: {r['definition']}" for r in result]

    def close(self):
        if self.driver:
            self.driver.close()

# Initialize Handler and LLM
kg_handler = Neo4jHandler()
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0.2
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "Query is required"}), 400

    print(f"Received query: {query}")

    # 1. Retrieve from KG
    try:
        facts = kg_handler.search(query)
    except Exception as e:
        print(f"Error searching KG: {e}")
        return jsonify({"error": "Database search failed"}), 500

    if not facts:
        return jsonify({
            "answer": "I could not find relevant content in the Knowledge Graph.",
            "sources": []
        })

    context = "\n---\n".join(facts)

    # 2. Generate answer
    messages = [
        SystemMessage(
            content=(
                "You are a helpful science teacher. "
                "Answer clearly and simply using ONLY the given knowledge graph context."
            )
        ),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion:\n{query}"
        )
    ]

    try:
        response = llm.invoke(messages)
        return jsonify({
            "answer": response.content,
            "sources": facts
        })
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting KG Flask Server on port 5001...")
    # Port 5001 to avoid conflict with RAG API on 5000
    app.run(host='0.0.0.0', port=5001, debug=True)

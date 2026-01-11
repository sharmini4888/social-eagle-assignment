import os
import sys
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Neo4j connection (using credentials from pdf-to-kg.py as default)
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "knowledge_graph_demo_2024")

class KGChatbot:
    def __init__(self):
        print("Initializing Knowledge Graph Chatbot...")
        try:
            self.driver = GraphDatabase.driver(
                NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
            )
            self.verify_connection()
        except Exception as e:
            print(f"❌ Failed to connect to Neo4j: {e}")
            sys.exit(1)

        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model="gpt-3.5-turbo",
            temperature=0.2
        )
        self.node_label = self.detect_node_label()

    def verify_connection(self):
        with self.driver.session() as session:
            result = session.run("RETURN 1 AS num")
            if result.single()["num"] == 1:
                print("✅ Connected to Neo4j successfully.")

    def detect_node_label(self):
        """Detect if we are using 'Concept' or other labels."""
        with self.driver.session() as session:
            # Check for Concept
            result = session.run("MATCH (n:Concept) RETURN count(n) as count")
            if result.single()["count"] > 0:
                print("ℹ️ Detected 'Concept' nodes (Simple Graph).")
                return "Concept"
            
            # Check for Entity
            result = session.run("MATCH (n:Entity) RETURN count(n) as count")
            if result.single()["count"] > 0:
                print("ℹ️ Detected 'Entity' nodes (Graphiti/Advanced Graph).")
                return "Entity"
            
            print("⚠️ No known nodes (Concept/Entity) found. The graph might be empty.")
            return None

    def search_graph(self, query):
        if not self.node_label:
            return []
        
        # Simple keyword search on 'name' property
        # In a real app, you'd want vector search or fulltext index.
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

    def chat_loop(self):
        print("\n🧠 Knowledge Graph Chatbot (type 'exit' to quit)")
        print("-" * 50)

        while True:
            user_input = input("\n❓ You: ").strip()
            
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue

            # 1. Retrieve from KG
            print("  🔍 Searching Knowledge Graph...")
            facts = self.search_graph(user_input)
            
            if not facts:
                print("🤖 Bot: I couldn't find relevant info in the Knowledge Graph.")
                continue

            context = "\n---\n".join(facts)
            
            # 2. Generate with LLM
            messages = [
                SystemMessage(content="You are a helpful assistant. Answer the user's question using ONLY the provided knowledge graph context."),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion:\n{user_input}")
            ]
            
            response = self.llm.invoke(messages)
            print(f"\n🤖 Bot: {response.content}")

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    bot = KGChatbot()
    try:
        bot.chat_loop()
    finally:
        bot.close()

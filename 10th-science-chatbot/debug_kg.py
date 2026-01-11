import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "knowledge_graph_demo_2024")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def debug_kg():
    with driver.session() as session:
        print("\n--- Node Counts ---")
        result = session.run("MATCH (n) RETURN labels(n) as labels, count(n) as count")
        for record in result:
            print(f"{record['labels']}: {record['count']}")

        print("\n--- First 20 Concept Nodes ---")
        result = session.run("MATCH (n:Concept) RETURN n.name as name LIMIT 20")
        for record in result:
            print(f"Prop 'name': {repr(record['name'])}")

        print("\n--- Search Test 'Light' ---")
        result = session.run("MATCH (n:Concept) WHERE toLower(n.name) CONTAINS 'light' RETURN n.name as name")
        found = list(result)
        print(f"Found {len(found)} matches for 'light'.")
        for f in found:
            print(f"Match: {repr(f['name'])}")

debug_kg()
driver.close()

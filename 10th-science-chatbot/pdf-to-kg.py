import os
import json
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from neo4j import GraphDatabase
from pyvis.network import Network

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Neo4j connection
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "knowledge_graph_demo_2024")

driver = GraphDatabase.driver(
    NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)
)

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0
)

def extract_concepts(text):
    """Extracts key scientific concepts and definitions/facts using LLM."""
    query = (
        "You are a helpful science assistant. "
        "Extract key scientific concepts (entities) and their relationships from the text below. "
        "Return the output strictly as a valid JSON object with two keys: "
        "'concepts' (a list of objects with 'name' and 'definition') and "
        "'relationships' (a list of objects with 'source', 'target', and 'relation'). "
        "Example: {"
        "  'concepts': [{'name': 'Photosynthesis', 'definition': 'Process by which plants make food.'}],"
        "  'relationships': [{'source': 'Photosynthesis', 'target': 'Sunlight', 'relation': 'REQUIRES'}]"
        "}"
        "\n\nText:\n" + text[:2000]
    )
    
    messages = [
        SystemMessage(content="Extract concepts and relationships as JSON."),
        HumanMessage(content=query)
    ]
    
    try:
        response = llm.invoke(messages)
        content = response.content.strip()
        # Handle potential markdown fencing
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        return json.loads(content)
    except Exception as e:
        print(f"Error extracting from chunk: {e}")
        return {"concepts": [], "relationships": []}

def store_in_neo4j(tx, data):
    # Data is expected to be a dict: {'concepts': [], 'relationships': []}
    
    # 1. Store Concepts
    concepts = data.get('concepts', [])
    for concept in concepts:
        name = concept.get('name')
        definition = concept.get('definition', "No definition provided.")
        
        if name:
            tx.run(
                """
                MERGE (c:Concept {name: $name})
                SET c.definition = $definition
                """,
                name=name,
                definition=definition
            )

    # 2. Store Relationships
    relationships = data.get('relationships', [])
    for rel in relationships:
        source = rel.get('source')
        target = rel.get('target')
        relation = rel.get('relation') # e.g., "CAUSES", "PART_OF"
        
        if source and target and relation:
            # We standardize relation to upper case just in case
            relation_type = relation.upper().replace(" ", "_")
            
            # Cypher query to merge relationship
            # Note: We can't parameterize the relationship type directly in MERGE with $type
            # So we use APOC or string formatting. For safety/simplicity here, we'll use a fixed query structure
            # or `call apoc.create.relationship`. 
            # Or simpler: just use a direct string injection if we trust LLM output (risky but okay for demo)
            # BETTER: Just use a generic type or sanitize. 
            # Let's sanitize simple alphanumeric.
            import re
            relation_type_safe = re.sub(r'[^A-Z0-9_]', '', relation_type)
            if not relation_type_safe:
                relation_type_safe = "RELATED_TO"

            query = (
                f"MATCH (a:Concept {{name: $source}}), (b:Concept {{name: $target}}) "
                f"MERGE (a)-[r:{relation_type_safe}]->(b) "
            )
            
            tx.run(query, source=source, target=target)

def visualize_graph():
    """Fetches graph from Neo4j and visualizes it using Pyvis."""
    print("🎨 Generating Graph Visualization...")
    net = Network(notebook=False, height="750px", width="100%", bgcolor="#222222", font_color="white")
    
    # Fetch all nodes and relationships
    with driver.session() as session:
        result = session.run("MATCH (n)-[r]->(m) RETURN n.name as source, r, m.name as target")
        
        # Keep track of added nodes to avoid duplicates in pyvis (though pyvis handles it, good optimization)
        added_nodes = set()
        
        for record in result:
            source = record['source']
            target = record['target']
            relation_type = record['r'].type
            
            if source not in added_nodes:
                net.add_node(source, title=source, color="#00ff1e") # Green for science!
                added_nodes.add(source)
            if target not in added_nodes:
                net.add_node(target, title=target, color="#00ff1e")
                added_nodes.add(target)
            
            net.add_edge(source, target, title=relation_type, label=relation_type)

    # Add physics buttons for fun interaction
    net.show_buttons(filter_=['physics'])
    output_file = "knowledge_graph.html"
    net.save_graph(output_file)
    print(f"✨ Visualization saved to: {os.path.abspath(output_file)}")

def main():
    print("🚀 Starting enhanced PDF to KG extraction...")
    
    # Load PDF
    loader = PyPDFLoader("science.pdf")
    docs = loader.load()
    print(f"📄 Loaded {len(docs)} pages.")

    with driver.session() as session:
        # Optional: Clear old Concept nodes to avoid duplicates/confusion?
        # session.run("MATCH (n:Concept) DETACH DELETE n") 
        # User said "check if there's something I missed", so maybe appending is safer or clearing is better?
        # Let's clear to ensure clean state for the demo.
        print("🧹 Clearing old Concept nodes...")
        session.run("MATCH (n:Concept) DETACH DELETE n")

        count = 0
        # Process first 20 pages for the demo to save time/tokens but get enough data
        # Skipping first few pages often contains TOC, so maybe 5-25
        # Modified to process fewer pages for testing as per plan
        for i, doc in enumerate(docs[5:7]): 
             print(f"Processing page {i+5}...")
             data = extract_concepts(doc.page_content)
             
             # Check if we got concepts
             c_list = data.get('concepts', [])
             r_list = data.get('relationships', [])
             
             if c_list:
                 session.execute_write(store_in_neo4j, data)
                 count += len(c_list)
                 print(f"   -> Stored {len(c_list)} concepts and {len(r_list)} relationships.")
            
    print(f"✅ Finished! Stored {count} concepts in Neo4j.")
    
    # Generate Visualization
    visualize_graph()
    
    driver.close()

if __name__ == "__main__":
    main()

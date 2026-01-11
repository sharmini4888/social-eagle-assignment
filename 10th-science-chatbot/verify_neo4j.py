from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "password"

try:
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run("RETURN 1 AS num")
        record = result.single()
        print(f"Connection successful! Result: {record['num']}")
    driver.close()
except Exception as e:
    print(f"Connection failed: {e}")

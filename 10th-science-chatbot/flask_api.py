import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("Initializing 10th Science RAG Chatbot API...")

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Load vector database
vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# Initialize LLM
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0.2
)

# Initialize Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "Query is required"}), 400

    print(f"Received query: {query}")

    # 1. Retrieve relevant chunks
    docs = vector_db.similarity_search(query, k=3)

    if not docs:
        return jsonify({
            "answer": "I could not find relevant content in your science book.",
            "sources": []
        })

    context = "\n\n".join([d.page_content for d in docs])

    # 2. Prepare prompt
    messages = [
        SystemMessage(
            content=(
                "You are a helpful science teacher for class 10 students. "
                "Answer clearly and simply using ONLY the given context."
            )
        ),
        HumanMessage(
            content=f"Context:\n{context}\n\nQuestion:\n{query}"
        )
    ]

    # 3. Generate answer
    try:
        response = llm.invoke(messages)
        return jsonify({
            "answer": response.content,
            "sources": [d.page_content for d in docs] 
        })
    except Exception as e:
        print(f"Error generating response: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)

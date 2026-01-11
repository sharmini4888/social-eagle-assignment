# ==================================================
# VECTOR SEARCH API (CHROMA DB) — UPDATED & SAFE
# ==================================================

from flask import Flask, request, jsonify
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

app = Flask(__name__)

# -------- LOAD CHROMA DB --------
embeddings = OpenAIEmbeddings()

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# -------- API ENDPOINT --------
@app.route("/vector-search", methods=["POST"])
def vector_search():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "query is required"}), 400

    docs = retriever.invoke(query)

    results = [
        {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in docs
    ]

    return jsonify({
        "query": query,
        "results": results
    })

if __name__ == "__main__":
    app.run(port=8001, debug=True)

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize embeddings
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Load vector database
vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

# Initialize LLM (OPENAI USED HERE 👇)
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0.2
)

print("🧪 Science RAG Chatbot (type 'exit' to quit)")
print("-" * 50)

while True:
    query = input("\n❓ You: ")

    if query.lower() in ["exit", "quit"]:
        print("👋 Goodbye, Scientist!")
        break

    # 1. Retrieve relevant chunks
    docs = vector_db.similarity_search(query, k=3)

    if not docs:
        print("🤖 Bot: I could not find relevant content in your science book.")
        continue

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
    response = llm.invoke(messages)

    print("\n🤖 Bot:")
    print(response.content)

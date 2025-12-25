# ===============================
# RAG + LLM + Web Validation
# Single File (Latest LangChain)
# ===============================

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.tools import DuckDuckGoSearchRun

# -------------------------------
# 1. Load Embeddings
# -------------------------------
embeddings = OpenAIEmbeddings()

# -------------------------------
# 2. Load Chroma Vector DB
# -------------------------------
vectorstore = Chroma(
    persist_directory="chroma_db",  # change if needed
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

print("✅ Chroma DB loaded successfully")

# -------------------------------
# 3. Load LLM
# -------------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# -------------------------------
# 4. RAG Prompt
# -------------------------------
rag_prompt = ChatPromptTemplate.from_template("""
You are an assistant answering questions strictly using the context below.

Context:
{context}

Question:
{question}

Answer clearly and concisely.
""")

# -------------------------------
# 5. Build RAG Chain (LCEL)
# -------------------------------
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
)

# -------------------------------
# 6. Web Search Tool
# -------------------------------
web_search = DuckDuckGoSearchRun()

# -------------------------------
# 7. Intelligent RAG + Validation
# -------------------------------
def intelligent_rag_answer(question: str):
    print("\n🔹 USER QUESTION:")
    print(question)

    # Step 1: RAG Answer
    rag_response = rag_chain.invoke(question)
    rag_answer = rag_response.content

    print("\n🔹 ANSWER FROM CHROMA (RAG):")
    print(rag_answer)

    # Step 2: Web Search
    web_result = web_search.run(question)

    print("\n🔹 WEB SEARCH RESULT:")
    print(web_result)

    # Step 3: Validate & Merge
    validation_prompt = f"""
    Question:
    {question}

    Answer from internal website data:
    {rag_answer}

    Answer from web search:
    {web_result}

    Task:
    - Validate correctness
    - Resolve conflicts
    - Merge both answers
    - Produce a final, accurate response
    """

    final_response = llm.invoke(validation_prompt)

    print("\n✅ FINAL VERIFIED ANSWER:")
    print(final_response.content)

# -------------------------------
# 8. Ask a Question
# -------------------------------
if __name__ == "__main__":
    intelligent_rag_answer(
        "What services does the website offer?"
    )

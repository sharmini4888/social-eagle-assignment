import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

st.set_page_config(page_title="6th Std English Chatbot", page_icon="📘")
st.title("📘 6th Standard English Chatbot")
st.write("Ask questions only from the English textbook")

# Load embeddings
embeddings = OpenAIEmbeddings()

# Load vector DB
vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

# Prompt
prompt = ChatPromptTemplate.from_template(
    """
    Answer the question using ONLY the context below.
    If the answer is not in the context, say "I don't know."

    Context:
    {context}

    Question:
    {question}
    """
)

# RAG chain (NEW STYLE)
rag_chain = (
    {
        "context": retriever,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask a question from the English book...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        answer = rag_chain.invoke(user_input)
        st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

import streamlit as st

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage


# ------------------------------------
# Streamlit Page
# ------------------------------------
st.set_page_config(page_title="Website Chatbot", layout="centered")
st.title("🤖 Website Chatbot")
st.write("Ask questions based on website content stored in Chroma DB")


# ------------------------------------
# Load Vector Store
# ------------------------------------
PERSIST_DIRECTORY = "./chroma_db"

embeddings = OpenAIEmbeddings()

vectorstore = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embeddings
)


# ------------------------------------
# Load LLM
# ------------------------------------
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)


# ------------------------------------
# User Input
# ------------------------------------
user_question = st.text_input("Type your question here 👇")


# ------------------------------------
# Button Action
# ------------------------------------
if st.button("Send"):
    if user_question.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):

            # 1️⃣ Retrieve top 5 relevant documents
            docs = vectorstore.similarity_search(user_question, k=5)

            # 2️⃣ Combine document content
            context = "\n\n".join([doc.page_content for doc in docs])

            # 3️⃣ Create prompt manually
            prompt = f"""
            Answer the question using ONLY the context below.

            Context:
            {context}

            Question:
            {user_question}
            """

            # 4️⃣ Ask LLM
            response = llm.invoke([HumanMessage(content=prompt)])

            answer = response.content

        st.success("Answer")
        st.write(answer)

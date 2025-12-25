from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
# Website URL you want to load
url = "https://buy2cash.com/pitchdeck/"

# Load website
loader = WebBaseLoader(url)
documents = loader.load()

print("Website loaded successfully!")
print("Number of documents:", len(documents))
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)

print("Text split into chunks")
print("Total chunks:", len(chunks))
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Data stored in Chroma DB successfully!")
# Access internal Chroma collection
collection = vectorstore._collection

# Get stored embeddings
results = collection.get(
    include=["embeddings", "documents"]
)

print("\nPrinting first 5 vectors:\n")

for i in range(5):
    print(f"Vector {i+1}:")
    print("Text:", results["documents"][i][:200], "...")  # first 200 chars
    print("Vector length:", len(results["embeddings"][i]))
    print("-" * 50)



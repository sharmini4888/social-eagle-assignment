from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

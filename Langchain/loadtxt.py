from langchain_community.document_loaders import TextLoader
loader = TextLoader("sample.txt")
documents = loader.load()
print(type(documents))        # <class 'list'>
print(type(documents[0]))     # <class 'langchain_core.documents.Document'>
print(documents[0].page_content)

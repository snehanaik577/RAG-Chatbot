from langchain_community.document_loaders import PyPDFLoader

# Load the PDF from the data folder
loader = PyPDFLoader("./data/Ebook-Agentic-AI.pdf")

# Read all pages into a list of Document objects
docs = loader.load()

print(f"✅ PDF loaded successfully, pages found: {len(docs)}")
print("----- First 300 characters of page 1 -----")
print(docs[0].page_content[:300])

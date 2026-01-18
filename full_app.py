import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from pinecone import ServerlessSpec, Pinecone

load_dotenv()

st.title("Agentic AI eBook RAG Chatbot - Setup Only")
st.write("This page only indexes the PDF. Use app.py for questions.")

def load_and_chunk_pdf(path: str):
    loader = PyPDFLoader(path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = splitter.split_documents(docs)
    return chunks

def init_pinecone_and_vectorstore():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not set")
    
    pc = Pinecone(api_key=api_key)
    index_name = "agentic-ai-ebook"
    
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws",region="us-east-1")
        )
    
    index = pc.Index(index_name)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
    return vectorstore

pdf_path = "./data/ebook.pdf"

st.subheader("1. Load and Chunk PDF")
if st.button("Load and chunk PDF"):
    chunks = load_and_chunk_pdf(pdf_path)
    st.write(f"✅ Loaded and split into {len(chunks)} chunks.")
    st.write("First chunk preview:")
    st.write(chunks[0].page_content[:300])

st.subheader("2. Index into Pinecone")
if st.button("Index chunks into Pinecone"):
    chunks = load_and_chunk_pdf(pdf_path)
    st.write(f"Indexing {len(chunks)} chunks into Pinecone...")
    vectorstore = init_pinecone_and_vectorstore()
    vectorstore.add_documents(chunks)
    st.success("✅ Finished indexing into Pinecone! Now use app.py for questions.")


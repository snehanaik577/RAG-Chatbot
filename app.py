import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

st.title("Agentic AI eBook RAG Chatbot")
st.write("Ask questions strictly from the Agentic AI eBook PDF.")

def init_retriever():
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not set")
    
    pc = Pinecone(api_key=api_key)
    index_name = "agentic-ai-ebook"
    index = pc.Index(index_name)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = PineconeVectorStore(index=index, embedding=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    return retriever

def answer_from_pdf(query: str):
    retriever = init_retriever()
    docs = retriever.invoke(query)
    
    context_text = "\n\n".join(
        [f"Source {i+1}:\n{d.page_content}" for i, d in enumerate(docs)]
    )
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    system_prompt = (
        "You are a helpful assistant that answers strictly from the "
        "provided Agentic AI eBook context. "
        "If the answer is not in the context, say "
        "'Insufficient information in the eBook.' "
        "Cite sources like (Source 1, Source 2)."
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": f"Question: {query}\n\nContext:\n{context_text}",
        },
    ]
    
    response = llm.invoke(messages)
    return response.content, docs

# Only Section 3: Ask a question
user_query = st.text_input("Ask about the Agentic AI eBook:")

if user_query:
    if st.button("Get answer"):
        with st.spinner("Thinking..."):
            answer, docs = answer_from_pdf(user_query)
        
        st.markdown("### Answer")
        st.write(answer)
        
        st.markdown("### Retrieved Context Chunks")
        for i, d in enumerate(docs):
            with st.expander(f"Source {i+1}"):
                st.write(d.page_content)

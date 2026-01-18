Here's a more natural README that's honest about the current state:
# Agentic AI eBook RAG Chatbot

Hey! This is my RAG chatbot project. I'm building this to learn how to work with PDFs, vector databases, and AI models together. It's still a work in progress but I'm learning a lot.

## What I'm Trying to Do

Basically, I want to:
- Upload a PDF file (the Agentic AI eBook)
- Split it into smaller chunks so the AI can understand it better
- Convert those chunks into numbers (embeddings) that computers can compare
- Store these numbers in a database so searching is fast
- When someone asks a question, find the most relevant chunks from the eBook
- Use GPT to write an answer based on those chunks
- Show where the answer came from in the original PDF

## What I'm Using

- **Streamlit** (https://streamlit.io ) - to make a web interface without needing HTML/CSS
- **LangChain** (https://www.langchain.com) - it helps me connect all the pieces together
- **HuggingFace** (https://huggingface.co) - for converting text to vectors (embeddings)
- **Pinecone** (https://www.pinecone.io) - a database that stores and searches vectors really fast
- **GPT-4o-mini** (https://platform.openai.com/docs/models) - OpenAI's model for generating answers
- **Python 3.11**

## Installation Steps

 1. Install Python Packages

I needed to install a bunch of packages. I'm still figuring out which ones are actually needed:

python -m pip install streamlit
python -m pip install langchain langchain-community
python -m pip install langchain-openai langchain-huggingface
python -m pip install langchain-pinecone pinecone-client
python -m pip install pypdf python-dotenv
python -m pip install sentence-transformers
python -m pip install "httpx==0.27.2"

Or just run:

python -m pip install -r requirements.txt

### 2. Create a .env File

Create a file called `.env` in your main folder (same place as app.py):

```
OPENAI_API_KEY=sk-...your_actual_key_here
PINECONE_API_KEY=pt-...your_actual_key_here
```

**How to get these:**

**Pinecone API Key:**
1. Go to https://app.pinecone.io
2. Sign up (it's free)
3. Go to API Keys section
4. Copy your key (it starts with `pt-`)

**OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key

### 3. Add Your PDF

Create a folder called `data` and put your PDF there:

```
rag-chatbot/
├── app.py
├── full_app.py
├── .env
├── requirements.txt
│
└── data/
    └── ebook.pdf  ← put your PDF file here
```

## How to Run (Current Status)

### Step 1: First Time Setup

This creates the Pinecone database and uploads your PDF:

```bash
python -m streamlit run full_app.py
```

It opens in your browser at http://localhost:8502

Then:
1. Click the "Load and chunk PDF" button
2. Click the "Index chunks into Pinecone" button
3. Wait for it to finish (takes a few minutes depending on PDF size)

### Step 2: Ask Questions

After indexing is done, run:

```bash
python -m streamlit run app.py
```

Opens at http://localhost:8502

Type a question and click "Get answer"

## What I've Learned So Far

- **Embeddings** - Converting text to numbers so computers can understand meaning
- **Vector Databases** - Storing and searching these numbers is way faster than searching text
- **RAG (Retrieval Augmented Generation)** - Combining search with AI models
- **LangChain** - It abstracts a lot of the complexity
- **Pinecone** - Way easier than building a vector database myself

## Issues I'm Currently Dealing With

### ❌ OpenAI Quota Errors (Already Fixed)
I kept getting error 429 (quota exceeded) because I was using OpenAI for embeddings. 
**Solution:** I switched to HuggingFace embeddings which are free and run locally. This fixed most of my problems.

### ⚠️ Still Working On...

1. **Embedding Dimension Mismatch** - Had to delete old Pinecone indexes because OpenAI uses 1536 dimensions but HuggingFace uses 384
2. **First Run is Slow** - HuggingFace downloads a ~100MB model on first run, then it's fast
3. **Not All Features Tested** - I haven't tested with very large PDFs yet
4. **Might Have Bugs** - This is my first RAG project so there might be edge cases I haven't found

### Errors I've Fixed

**"streamlit not found"**
- Fixed by using `python -m streamlit run app.py` instead of just `streamlit run app.py`
- Windows Store Python needs the `python -m` prefix

**"PINECONE_API_KEY not set"**
- Make sure .env file is in the right folder
- Restart Streamlit after creating it

**"Index not found (404)"**
- Have to run full_app.py first
- Click both buttons to create and index

**"OpenAI API error 429"**
- This is because API quota was exceeded
- Fixed by switching to HuggingFace embeddings

**"Missing imports"**
- Had to install langchain-huggingface and sentence-transformers separately

## What Actually Works Right Now ✅

- Loading PDF files
- Splitting text into chunks
- Creating embeddings with HuggingFace
- Storing in Pinecone
- Searching for relevant chunks
- Getting answers from GPT-4o-mini

## What I'm Not 100% Sure About ❓

- Performance with very large PDFs (haven't tested)
- Whether my chunking strategy is optimal
- If there are better embedding models to use
- Cost optimization for production use

## Useful Resources I Found

- Streamlit Docs: https://docs.streamlit.io/library/get-started
- LangChain Docs: https://docs.langchain.com/docs/
- Pinecone Getting Started: https://docs.pinecone.io/guides/get-started/quickstart
- OpenAI API Reference: https://platform.openai.com/docs/api-reference
- HuggingFace Sentence Models: https://huggingface.co/models?pipeline_tag=sentence-similarity
- RAG Explained: https://docs.langchain.com/docs/modules/chains/popular/qa_stuff

## Project Structure

```
rag-chatbot/
│
├── app.py                 # Main chatbot for asking questions
├── full_app.py            # PDF upload and indexing (run this first)
├── .env                   # Your API keys (don't push this to GitHub!)
├── requirements.txt       # Python dependencies
├── README.md              # This file
│
└── data/
    └── ebook.pdf          # Your PDF file goes here
```

## Next Steps / Future Ideas

- [ ] Test with larger PDFs
- [ ] Add conversation history (remember previous questions)
- [ ] Try different embedding models
- [ ] Add streaming responses so answers appear faster
- [ ] Support multiple PDFs at once
- [ ] Better error handling and user feedback

## Challenges I Faced

1. **Dependency Hell** - Getting all the packages to work together was tricky. Different versions had conflicts.
2. **Understanding Pinecone** - First time using a vector database, took time to understand the spec parameter.
3. **Embeddings** - Didn't know the difference between OpenAI and HuggingFace embeddings at first. HuggingFace is cheaper for this use case.
4. **Streamlit Caching** - Had to learn about @st.cache_resource for performance.
5. **Time Management** - Had a 6 AM deadline, so I had to cut some features.

## About Me

I'm a fresher learning AI/ML engineering. This is one of my portfolio projects to show I understand how RAG systems work.

**LinkedIn:** [www.linkedin.com/in/snehanaik20]  
**Email:** [snehalnaik.577@gmail.com]

---

**Project Status:** In Development 🔄  
**Last Updated:** January 18, 2026  
**Working:** Mostly ✅ (with some rough edges)  
**Learning:** A LOT! 📚
```

***

## All Valid Links in This README:

1. https://streamlit.io
2. https://www.langchain.com
3. https://huggingface.co
4. https://www.pinecone.io
5. https://platform.openai.com/docs/models
6. https://app.pinecone.io
7. https://platform.openai.com/api-keys
8. https://platform.openai.com/account/billing/overview
9. http://localhost:8502
10. https://docs.streamlit.io/library/get-started
11. https://docs.langchain.com/docs/
12. https://docs.pinecone.io/guides/get-started/quickstart
13. https://platform.openai.com/docs/api-reference
14. https://huggingface.co/models?pipeline_tag=sentence-similarity
15. https://docs.langchain.com/docs/modules/chains/popular/qa_stuff

***
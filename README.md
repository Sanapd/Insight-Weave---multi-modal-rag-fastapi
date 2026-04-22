# 📘 Insight-Weave: Multi-Modal RAG FastAPI System

Insight-Weave is an end-to-end Retrieval-Augmented Generation (RAG) system that enables intelligent question answering over PDF documents by extracting text, tables, formulas, and images, generating embeddings, storing them in a vector database, and retrieving relevant context using an LLM.

This project integrates FastAPI, Pinecone, SentenceTransformers, Azure Blob Storage, and LLaMA-3 (Groq API) to deliver context-aware responses with citations.

---

# 🚀 Features

- PDF ingestion from Azure Blob Storage
- Extracts text, tables, formulas, and images
- Converts tables into markdown format
- Detects mathematical formulas automatically
- Generates embeddings using SentenceTransformers
- Stores vectors in Pinecone vector database
- Retrieval-based answering using LLaMA-3 (Groq API)
- FastAPI backend with interactive UI
- Context-aware responses with citations
- Multi-modal document understanding pipeline

---

# 🧠 System Architecture

Pipeline workflow:

PDF (Azure Blob Storage)
↓
Text + Tables + Formulas + Images Extraction
↓
Chunking + Cleaning
↓
SentenceTransformer Embeddings
↓
Pinecone Vector Database
↓
Context Retrieval
↓
LLaMA-3 (Groq API)
↓
FastAPI Response UI

---

# 🛠️ Tech Stack

Backend:
- FastAPI
- Python

Vector Database:
- Pinecone

Embedding Model:
- SentenceTransformers (all-MiniLM-L6-v2)

LLM:
- LLaMA-3 (Groq API)

Cloud Storage:
- Azure Blob Storage

Document Processing:
- PyMuPDF
- pdfplumber
- LangChain Text Splitters

Environment Management:
- python-dotenv

---

# 📂 Project Structure

Insight-Weave/
│
├── app.py
├── main.py
├── chat_app.py
├── chunking.py
├── embedding.py
├── formulas.py
├── img.py
├── table.py
├── vector_store.py
├── Read_data.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── .env (not uploaded for security)

---

# ▶️ How to Run the Project

Step 1: Clone repository

git clone https://github.com/Sanapd/Insight-Weave---multi-modal-rag-fastapi.git

Step 2: Install dependencies

pip install -r requirements.txt

Step 3: Add environment variables

Create `.env` file and add required API keys

Step 4: Run application

python app.py

Open browser:

http://127.0.0.1:8000

---

# 📊 Applications

This system can be used for:

- Document Question Answering
- Research Assistant Systems
- Enterprise Knowledge Retrieval
- Technical PDF Analysis
- Academic Content Search
- Multi-modal Semantic Search Engines

---

# 💡 Key Highlights

- End-to-end GenAI pipeline
- Multi-modal document understanding
- Vector search implementation
- Cloud storage integration
- Production-style FastAPI backend
- Retrieval-Augmented LLM workflow

---

# 📈 Future Improvements

- Support multiple PDFs
- Add hybrid search (BM25 + vector search)
- Deploy on AWS / Azure
- Add authentication layer
- Add Streamlit dashboard

---

# 👩‍💻 Author

Bhumika Sanap  
AI / ML Enthusiast | Data Analyst | Generative AI Projects

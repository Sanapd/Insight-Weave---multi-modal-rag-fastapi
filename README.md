# Insight Weave - Multi-modal RAG FastAPI Project

This project is a Retrieval-Augmented Generation (RAG) system that extracts and retrieves information from PDF documents using embeddings and a vector database. It supports multiple data types including text, tables, formulas, and images.

## Features

- PDF ingestion from Azure Blob Storage
- Extracts text, tables, formulas, and images
- Converts tables into markdown format
- Generates embeddings using SentenceTransformers
- Stores embeddings in Pinecone vector database
- Retrieval-based answering using LLaMA-3 (Groq API)
- FastAPI backend with interactive UI
- Context-aware responses with citations

## Tech Stack

Python  
FastAPI  
SentenceTransformers  
Pinecone Vector Database  
Groq LLaMA-3  
Azure Blob Storage  
PyMuPDF  
LangChain Text Splitter  

## Project Workflow

1. Download PDF from Azure Blob Storage
2. Extract text, tables, formulas, and images
3. Generate embeddings
4. Store vectors in Pinecone
5. Retrieve relevant context
6. Generate responses using LLaMA-3
7. Display results through FastAPI interface

## How to Run the Project

Install dependencies:

pip install -r requirements.txt

Run server:

python app.py

Open browser:

http://127.0.0.1:8000

## Applications

Document Question Answering System  
Research Assistant  
Knowledge Retrieval System  
Enterprise Document Search

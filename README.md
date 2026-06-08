# rag_chatbot
# RAG Capital Chatbot

A simple Retrieval-Augmented Generation (RAG) chatbot built to understand and implement the core concepts of modern AI retrieval systems.

The chatbot retrieves information about countries and their capitals from a knowledge base and uses a Large Language Model (LLM) to generate responses grounded in the retrieved context.

This project was developed as a learning exercise to explore vector databases, embeddings, document retrieval, and prompt augmentation workflows used in production RAG systems.

## Features

- Retrieval-Augmented Generation (RAG) pipeline
- Vector-based document search
- Embedding generation for country-capital knowledge base
- Context-aware responses
- Simple chatbot interface
- Source-grounded answers

## Tech Stack

- Python
- LangChain
- ChromaDB / FAISS
- OpenAI / Ollama / Gemini
- Sentence Transformers
- Streamlit

## Architecture

User Query
↓
Embedding Generation
↓
Vector Database Search
↓
Top-K Relevant Documents Retrieved
↓
Context Augmentation
↓
LLM Response Generation
↓
Answer Returned to User

## Project Structure

├── data/
│ └── capitals.pdf
├── create_embeddings.pdf
├── app.py
├── extract_pdf.py
├── requirements.txt
└── README.md

## Installation

### Clone Repository

git clone https://github.com/yourusername/rag-capital-chatbot.git

cd rag-capital-chatbot

### Create Virtual Environment

python -m venv venv

### Activate Environment

# Windows

venv\Scriptsa\activate

# Linux/Mac

source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Run Application

python app.py

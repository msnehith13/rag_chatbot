# rag_chatbot
# 📄 AI Research Paper Assistant

A **Retrieval-Augmented Generation (RAG)** chatbot that lets you upload any research paper (PDF) and have an intelligent, memory-persistent conversation with it — powered by **Groq + LLaMA 3.3**, **FAISS vector search**, and **Google OAuth**.

---

## ✨ Features

- 🔐 **Google OAuth Login** — Sign in with your Google account, no passwords stored
- 📄 **PDF Upload & Parsing** — Extracts and indexes any research paper using PyMuPDF
- 🧠 **RAG Pipeline** — Retrieves relevant chunks via FAISS before generating answers
- 💬 **Persistent Chat Sessions** — All conversations saved to SQLite, resumable anytime
- 📊 **Evaluation Dashboard** — Auto-scores every response on Relevance, Completeness & Confidence
- ⬇️ **CSV Export** — Download your full evaluation report for offline analysis
- ⚡ **Fast Responses** — LLaMA 3.3 70B via Groq API (~2 second response time)

---

## 🏗️ Architecture

```
PDF Upload
    │
    ▼
PyMuPDF (text extraction)
    │
    ▼
Chunking (500 words, overlapping)
    │
    ▼
Sentence Transformers (all-MiniLM-L6-v2) → 384-dim vectors
    │
    ▼
FAISS Index (similarity search)
    │
    ▼
User Question → Embed → Retrieve Top-4 Chunks
    │
    ▼
Groq API (LLaMA 3.3 70B) → Answer
    │
    ▼
Evaluator → Relevance + Completeness + Confidence scores
    │
    ▼
SQLite (persist messages + scores)
```

---

## 📁 Project Structure

```
research_analyzer/
├── app.py              # Main Streamlit app — UI, auth, chat, dashboard
├── extractor.py        # PDF text extraction + chunking (PyMuPDF)
├── vector_store.py     # FAISS index builder + similarity retrieval
├── evaluator.py        # RAG evaluation metrics (relevance, completeness, confidence)
├── db.py               # SQLite database — users, sessions, messages, evaluations
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

> `research_assistant.db` is auto-generated on first run.

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.10+
- A free [Groq API key](https://console.groq.com)
- A [Google Cloud OAuth 2.0 client](https://console.cloud.google.com) (Client ID + Secret)

---

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/research-analyzer.git
cd research-analyzer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API keys

Open `app.py` and update the following constants near the top:

```python
client = Groq(api_key="your_groq_api_key_here")          # From console.groq.com

GOOGLE_CLIENT_ID     = "your_google_client_id"            # From Google Cloud Console
GOOGLE_CLIENT_SECRET = "your_google_client_secret"
```

### 4. Google OAuth Setup (one-time)

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → **APIs & Services** → **OAuth consent screen** → External
3. Go to **Credentials** → **+ Create Credentials** → **OAuth 2.0 Client ID**
4. Application type: **Web application**
5. Add the following:
   - **Authorized JavaScript Origins:** `http://localhost:8501`
   - **Authorized Redirect URIs:** `http://localhost:8501/oauth2callback`
6. Copy the **Client ID** and **Client Secret** into `app.py`
7. Under **OAuth consent screen → Test users**, add your Gmail address

### 5. Run the app

```bash
python -m streamlit run app.py
```

Open your browser at **http://localhost:8501**

---

## 📦 Requirements

```
streamlit
groq
pymupdf
faiss-cpu
sentence-transformers
streamlit-oauth
httpx
pandas
```

Install all at once:

```bash
pip install streamlit groq pymupdf faiss-cpu sentence-transformers streamlit-oauth httpx pandas
```

---

## 🚀 Usage Guide

### 1. Login
Click **"Continue with Google"** and sign in with your Gmail account.

### 2. Create a Session
- Enter a session name (e.g. `Attention Is All You Need`)
- Upload a research paper PDF
- Click **"Create Session & Process PDF"**

### 3. Ask Questions
Type any question about the paper in the chat input. Examples:
- *"What problem does this paper solve?"*
- *"What methodology did the authors use?"*
- *"What were the key results or benchmarks?"*

### 4. View Source Chunks
Expand **"📚 Source chunks used"** below any answer to see the exact passages retrieved from the paper.

### 5. Check Evaluation Scores
Each answer shows three auto-computed scores:

| Metric | Method | Meaning |
|---|---|---|
| **Relevance** | Cosine similarity | How aligned retrieved chunks are with the question |
| **Completeness** | LLM-as-judge | How fully the answer addresses the question |
| **Confidence** | Weighted average | Overall response quality (40% relevance + 60% completeness) |

### 6. Evaluation Dashboard
Click **📊 Metrics** in the sidebar to see:
- Overall averages across all sessions
- Score trend chart over time
- Per-session breakdown
- CSV export button

### 7. Resume Sessions
Sign out and back in — all your sessions are saved and ready to resume from the sidebar.

---

## 🔒 Security Notes

- Passwords are **never stored** — authentication is delegated entirely to Google
- Only your Google user ID, name, email and conversation history are stored locally
- Your Groq API key and Google Client Secret should **never be committed to Git**
- Add a `.gitignore` entry for your secrets:

```gitignore
research_assistant.db
.env
```

> ⚠️ **Rotate your Google Client Secret** if it was ever exposed publicly.

---

## 📊 Evaluation Metric Details

### Relevance Score
```
cosine_similarity(embed(question), mean(embed(chunks)))
```
Purely mathematical — no API call. Scores how topically aligned the retrieved chunks are with the question.

### Completeness Score
A second Groq API call asks LLaMA 3.3:
> *"Does this answer fully address the question? Return JSON: {"score": 0.0–1.0}"*

### Confidence Score
```
confidence = 0.4 × relevance + 0.6 × completeness
```

Score labels: **Excellent** (≥80%) · **Good** (≥65%) · **Fair** (≥45%) · **Poor** (<45%)

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| `streamlit` not recognized | Use `python -m streamlit run app.py` |
| Blank page on load | Hard refresh with `Ctrl+Shift+R` |
| Model decommissioned error | Change `GROQ_MODEL` to `"llama-3.3-70b-versatile"` in `app.py` |
| Google OAuth redirect error | Ensure redirect URI is exactly `http://localhost:8501/oauth2callback` |
| Slow first response | Normal — Sentence Transformer model downloads ~90MB on first run |
| DB schema error | Delete `research_assistant.db` and restart |

---

## 🔮 Future Improvements

- [ ] Multi-paper sessions — query across multiple PDFs simultaneously
- [ ] Citation extraction — auto-list all references from a paper
- [ ] RAGAS integration — industry-standard RAG evaluation framework
- [ ] Streamlit Cloud deployment — publicly accessible URL
- [ ] PDF annotation — highlight retrieved sentences in the original document
- [ ] Semantic chunking — split by meaning rather than fixed word count

---

## 📚 Tech Stack

| Library | Purpose |
|---|---|
| [PyMuPDF](https://pymupdf.readthedocs.io/) | PDF text extraction |
| [Sentence Transformers](https://www.sbert.net/) | Text embeddings (all-MiniLM-L6-v2) |
| [FAISS](https://faiss.ai/) | Vector similarity search |
| [Groq](https://console.groq.com/) | LLM inference (LLaMA 3.3 70B) |
| [Streamlit](https://streamlit.io/) | Web UI framework |
| [streamlit-oauth](https://github.com/dnplus/streamlit-oauth) | Google OAuth 2.0 |
| [SQLite](https://www.sqlite.org/) | Persistent storage |
| [httpx](https://www.python-httpx.org/) | Google userinfo API calls |
| [pandas](https://pandas.pydata.org/) | Evaluation data processing |

---

## 🤝 Acknowledgements

- [Meta AI](https://ai.meta.com/) for LLaMA 3.3
- [Groq](https://groq.com/) for free, fast LLM inference
- [Hugging Face](https://huggingface.co/) for Sentence Transformers
- [Facebook AI Research](https://ai.facebook.com/) for FAISS

---

*Built as an academic project demonstrating production-grade RAG system design.*

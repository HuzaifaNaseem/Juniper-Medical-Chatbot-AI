# Juniper — Medical AI Research Assistant

A RAG-powered chatbot that answers medical questions by searching an embedded knowledge base — grounded in retrieved context, not hallucination.

Live at: [juniper-portfolio.netlify.app](https://juniper-portfolio.netlify.app/)

---

## What Problem It Solves

Patients and researchers spend hours parsing dense medical literature. Juniper lets them ask plain-English questions and get concise, sourced answers drawn from a structured medical knowledge base — in English or Roman Urdu.

---

## Features

- **RAG architecture** — Retrieval-Augmented Generation using ChromaDB vector store + Groq LLM
- **Embedded knowledge base** — 50+ medical topics (cardiovascular, oncology, neurology, pharmacology, and more) loaded at startup, no file uploads needed
- **Multi-turn conversations** — context-aware responses across the full conversation history
- **Bilingual support** — responds in English or Roman Urdu based on query language
- **User authentication** — register/login with session management (SQLite-backed)
- **Health check endpoint** — `/api/health` for uptime monitoring

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| LLM | Groq API (Llama 3.3 70B) |
| Vector store | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Auth | SQLite + session tokens |
| Frontend | HTML, CSS, Vanilla JS |
| Deployment | Gunicorn + Supervisor |

---

## Screenshots

<!-- Add screenshots here -->

---

## Getting Started

### Prerequisites

- Python 3.8+
- A free Groq API key — [console.groq.com](https://console.groq.com)

### Installation

```bash
git clone https://github.com/HuzaifaNaseem/Juniper-Medical-Chatbot-AI.git
cd Juniper-Medical-Chatbot-AI/Juniper-Medical-Chatbot-AI--master
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Setup

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY and a generated SECRET_KEY
```

Generate a SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Initialize Knowledge Base & Run

```bash
python initialize_kb.py
python app.py
```

App runs at `http://localhost:8080`

---

## Project Structure

```
├── app.py                  # Flask app entry point
├── config.py               # Environment-based configuration
├── initialize_kb.py        # Loads medical knowledge into ChromaDB
├── backend/
│   ├── llm_service.py      # Groq API integration
│   ├── rag_engine.py       # Retrieval + generation pipeline
│   ├── vector_store.py     # ChromaDB wrapper
│   ├── knowledge_base.py   # Embedded medical content
│   └── user_auth.py        # Auth and session management
├── static/                 # CSS + JS assets
├── templates/              # HTML templates
├── requirements.txt
└── .env.example
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (required) |
| `SECRET_KEY` | Flask session secret (generate a random string) |
| `FLASK_ENV` | `development` or `production` |
| `CORS_ORIGINS` | Allowed origins, default `*` |

---

## License

MIT

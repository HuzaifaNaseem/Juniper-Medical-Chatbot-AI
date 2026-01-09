# Juniper - Medical Research Assistant

![Juniper](https://img.shields.io/badge/Status-Production-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-lightgrey)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

**Juniper** is a production-level Retrieval-Augmented Generation (RAG) chatbot designed for medical research assistance. Built with Python, Flask, and advanced LLM technology, Juniper provides accurate, context-aware responses to medical queries using an embedded knowledge base.

## Features

- **RAG Architecture**: Combines vector search with LLM generation for accurate responses
- **Embedded Knowledge Base**: Pre-loaded with 100+ medical topics (no external files needed)
- **Modern UI**: Professional, responsive interface with conversation history
- **Free-Tier LLM**: Uses Groq's Llama 3.1 70B (ultra-fast, free API)
- **Local Embeddings**: sentence-transformers for semantic search
- **Conversation Memory**: Context-aware multi-turn conversations
- **Zero Setup**: Works immediately after deployment

## Domain: Medical Research

Juniper specializes in:
- Disease information and pathology
- Symptoms and diagnosis
- Treatment options and procedures
- Preventive medicine
- Medical terminology
- Drug information

## Technology Stack

### Backend
- **Framework**: Flask 3.0
- **Vector Store**: ChromaDB
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)
- **LLM**: Groq API (Llama 3.1 70B)
- **Language**: Python 3.8+

### Frontend
- **HTML5** with semantic markup
- **CSS3** with modern animations
- **Vanilla JavaScript** (no frameworks)
- **Responsive Design** (mobile-first)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Groq API key (free at https://console.groq.com)

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/juniper-rag.git
cd juniper-rag
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the knowledge base**
```bash
python initialize_kb.py
```

5. **Run the application**
```bash
python app.py
```

6. **Access the application**
Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
JUNIPER-RAG/
├── app.py                 # Flask application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
├── initialize_kb.py      # Knowledge base initialization script
│
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── script.js     # Frontend JavaScript
│   └── images/
│       └── logo.png      # Juniper logo
│
├── templates/
│   └── index.html        # Main HTML template
│
├── backend/
│   ├── __init__.py
│   ├── rag_engine.py     # RAG implementation
│   ├── llm_service.py    # LLM integration
│   ├── vector_store.py   # ChromaDB wrapper
│   └── knowledge_base.py # Embedded medical data
│
├── data/
│   └── chroma_db/        # ChromaDB storage (auto-generated)
│
└── docs/
    ├── ARCHITECTURE.md   # System architecture
    ├── API.md           # API documentation
    └── DEPLOYMENT.md    # Deployment guide
```

## Usage

### Basic Conversation
1. Open Juniper in your browser
2. Type a medical question in the input field
3. Press Enter or click Send
4. Juniper will retrieve relevant information and generate a response

### Example Queries
- "What are the symptoms of diabetes?"
- "Explain how antibiotics work"
- "What is the difference between Type 1 and Type 2 diabetes?"
- "Tell me about cardiovascular disease prevention"

## Architecture

### RAG Pipeline
1. **User Query** → Frontend sends to Flask API
2. **Embedding** → Query converted to vector using sentence-transformers
3. **Retrieval** → Top-k relevant documents fetched from ChromaDB
4. **Context Building** → Retrieved documents formatted as context
5. **Generation** → Groq LLM generates response using context
6. **Response** → Answer sent back to frontend

### Key Components
- **Vector Store**: ChromaDB with cosine similarity search
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **LLM**: Llama 3.1 70B via Groq (8k context window)
- **Chunk Size**: 500 tokens with 50 token overlap
- **Top-K Retrieval**: 5 most relevant documents

## API Endpoints

### POST /api/chat
Send a message to Juniper

**Request:**
```json
{
  "message": "What are the symptoms of diabetes?",
  "conversation_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Juniper's answer...",
  "conversation_id": "session-123",
  "sources": ["doc1", "doc2"],
  "timestamp": "2025-01-06T10:30:00Z"
}
```

### GET /api/health
Check system health and status

## Deployment

### Vercel (Recommended)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel`
3. Add environment variables in Vercel dashboard

### Render
1. Connect GitHub repository
2. Select "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python app.py`
5. Add environment variables

### Docker
```bash
docker build -t juniper-rag .
docker run -p 5000:5000 --env-file .env juniper-rag
```

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # Windows: set FLASK_ENV=development
python app.py
```

### Adding Medical Content
Edit `backend/knowledge_base.py` to add new medical topics:
```python
MEDICAL_KNOWLEDGE = [
    {
        "title": "New Disease",
        "content": "Detailed information...",
        "category": "diseases"
    }
]
```

Then re-initialize: `python initialize_kb.py`

## Testing

### Run Unit Tests
```bash
pytest tests/
```

### Manual Testing
Use the included test queries in `tests/test_queries.txt`

## Acknowledgments

- Groq for providing free LLM API access
- Sentence-Transformers for embedding models
- ChromaDB for vector storage
- Flask community for excellent documentation

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Email: huzaifakhan654916@gmail.com

## Roadmap

- [ ] Add more medical specialties
- [ ] Implement user authentication
- [ ] Add export conversation feature
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Mobile app


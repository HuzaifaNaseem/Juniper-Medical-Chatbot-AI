# Juniper - Complete Setup Guide

This guide will walk you through setting up Juniper from scratch on your local machine.

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.8+** installed ([Download here](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for cloning)
- **Groq API Key** (free, get it at [console.groq.com](https://console.groq.com))

## 🚀 Step-by-Step Installation

### Step 1: Get a Groq API Key (FREE)

1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Click "Create API Key"
5. Copy your API key (you'll need this soon)

**Note:** Groq offers free API access with generous limits - perfect for this project!

### Step 2: Navigate to Project Directory

Open your terminal/command prompt and navigate to the project directory:

```bash
cd c:\Users\defaultuser0\OneDrive\Desktop\JUNIPER-RAG
```

Or wherever you've placed the project.

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages:
- Flask (web framework)
- sentence-transformers (embeddings)
- chromadb (vector database)
- groq (LLM API)
- And more...

**Note:** This may take 5-10 minutes depending on your internet speed.

### Step 5: Create Environment File

Create a file named `.env` in the project root directory:

**Windows (Command Prompt):**
```bash
copy .env.example .env
```

**Mac/Linux:**
```bash
cp .env.example .env
```

Now edit the `.env` file with a text editor and add your Groq API key:

```env
FLASK_ENV=production
SECRET_KEY=juniper-secret-key-change-this-in-production
GROQ_API_KEY=your_actual_groq_api_key_here
CORS_ORIGINS=*
```

**Replace `your_actual_groq_api_key_here` with the API key you got in Step 1!**

### Step 6: Initialize the Knowledge Base

This is a crucial step that sets up the medical knowledge database:

```bash
python initialize_kb.py
```

**What this does:**
- Loads 50+ medical topics into memory
- Generates embeddings using sentence-transformers
- Stores everything in ChromaDB vector database
- Creates the `data/chroma_db` directory

**Expected output:**
```
============================================================
JUNIPER - Medical Knowledge Base Initialization
============================================================

Configuration:
  Database Path: ./data/chroma_db
  Collection Name: medical_knowledge
  Embedding Model: sentence-transformers/all-MiniLM-L6-v2
  Total Medical Topics: 50

[1/3] Initializing vector store...
✓ Vector store initialized

[2/3] Preparing documents...
✓ Prepared 50 documents

[3/3] Adding documents to vector store...
[Progress bar...]
✓ Documents added successfully

============================================================
INITIALIZATION COMPLETE
============================================================

✓ Juniper knowledge base is ready!
```

**⏱️ This takes 2-5 minutes on first run** (downloads embedding model and processes documents).

### Step 7: Run the Application

```bash
python app.py
```

**Expected output:**
```
============================================================
🌿 JUNIPER - Medical Research Assistant
============================================================

Environment: production
Debug Mode: False
Model: llama-3.1-70b-versatile

Initializing RAG engine...
Loading vector store...
✓ Vector store initialized
Initializing LLM service...
✓ LLM service initialized

✓ System initialized successfully
============================================================

🚀 Starting server on http://localhost:5000
Press CTRL+C to stop
```

### Step 8: Access Juniper

Open your web browser and go to:
```
http://localhost:5000
```

You should see the Juniper interface! 🎉

## ✅ Testing Your Installation

Try these sample queries:

1. "What are the symptoms of diabetes?"
2. "Explain how antibiotics work"
3. "What is cardiovascular disease?"
4. "Tell me about the immune system"

Juniper should respond with detailed, accurate medical information!

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:** You didn't activate the virtual environment. Run:
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

Then reinstall: `pip install -r requirements.txt`

### Issue: "Vector store is empty"

**Solution:** You forgot to initialize the knowledge base. Run:
```bash
python initialize_kb.py
```

### Issue: "Failed to connect to Groq API"

**Solutions:**
1. Check your `.env` file has the correct API key
2. Verify the API key is active at [console.groq.com](https://console.groq.com)
3. Check your internet connection
4. Make sure no spaces around the `=` sign in `.env`:
   ```
   GROQ_API_KEY=gsk_abc123...  ✓ Correct
   GROQ_API_KEY = gsk_abc123... ✗ Wrong
   ```

### Issue: Port 5000 already in use

**Solution:** Change the port in `app.py` or set environment variable:
```bash
# Windows
set PORT=8000

# Mac/Linux
export PORT=8000

python app.py
```

### Issue: "Torch not compiled with CUDA"

**This is normal!** The app will use CPU for embeddings, which is fine for this project. It might be slightly slower but works perfectly.

## 📊 Verify Everything is Working

### Check Health Endpoint

Open a new terminal and run:

**Windows (PowerShell):**
```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/health | Select-Object -Expand Content
```

**Mac/Linux:**
```bash
curl http://localhost:5000/api/health
```

You should see:
```json
{
  "status": "healthy",
  "stats": {
    "vector_store_stats": {
      "document_count": 50,
      ...
    }
  }
}
```

## 🎓 Next Steps

Now that Juniper is running:

1. **Test thoroughly** with various medical queries
2. **Customize** the knowledge base (add more topics in `backend/knowledge_base.py`)
3. **Deploy** to the internet (see DEPLOYMENT.md)
4. **Share** your project on GitHub!

## 📁 Project Structure Overview

```
JUNIPER-RAG/
├── app.py                    # Main Flask application
├── initialize_kb.py          # Knowledge base setup script
├── config.py                 # Configuration
├── requirements.txt          # Dependencies
├── .env                      # Your API keys (DON'T COMMIT THIS!)
│
├── templates/
│   └── index.html           # Frontend HTML
│
├── static/
│   ├── css/style.css        # Styles
│   └── js/script.js         # Frontend JavaScript
│
├── backend/
│   ├── knowledge_base.py    # Medical knowledge data
│   ├── vector_store.py      # ChromaDB wrapper
│   ├── llm_service.py       # Groq API integration
│   └── rag_engine.py        # RAG orchestration
│
└── data/
    └── chroma_db/           # Vector database (auto-generated)
```

## 🔥 Quick Commands Reference

```bash
# Activate virtual environment
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Initialize knowledge base
python initialize_kb.py

# Run application
python app.py

# Deactivate virtual environment
deactivate
```

## 💡 Tips

1. **Keep your virtual environment activated** while working on the project
2. **Don't commit `.env` file** to Git (it contains your API key)
3. **The first run takes longer** because it downloads the embedding model
4. **Subsequent runs are fast** because everything is cached

## 🎯 Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] `.env` file created with Groq API key
- [ ] Knowledge base initialized (ran `python initialize_kb.py`)
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Test query returns medical information

## 📞 Need Help?

If you're stuck:
1. Check the troubleshooting section above
2. Read the error messages carefully
3. Verify each step was completed
4. Check your Python version: `python --version`
5. Check if venv is activated (you should see `(venv)` in terminal)

---

**You're all set! Enjoy using Juniper! 🌿**

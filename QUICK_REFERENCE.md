# Juniper - Quick Reference Card

## 🚀 Quick Start (Windows)

```bash
# Just double-click this file:
quick_start.bat
```

## 🚀 Quick Start (Mac/Linux)

```bash
# Run this command:
./quick_start.sh
```

## 📦 Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# 5. Edit .env and add your Groq API key
# Get free key at: https://console.groq.com

# 6. Initialize knowledge base
python initialize_kb.py

# 7. Run the app
python app.py
```

## 🔑 Get Groq API Key (FREE)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Click "Create API Key"
4. Copy key to `.env` file

## 📝 Project Structure

```
JUNIPER-RAG/
├── app.py                 # ← Main app (run this)
├── initialize_kb.py       # ← Run once to setup
├── config.py             # Configuration
├── requirements.txt      # Dependencies
├── .env                  # ← Add your API key here
│
├── templates/
│   └── index.html       # Frontend
│
├── static/
│   ├── css/style.css    # Styles
│   └── js/script.js     # Frontend logic
│
└── backend/
    ├── knowledge_base.py  # Medical data (50+ topics)
    ├── vector_store.py    # ChromaDB
    ├── llm_service.py     # Groq API
    └── rag_engine.py      # RAG logic
```

## 🔧 Common Commands

```bash
# Start app
python app.py

# Initialize knowledge base
python initialize_kb.py

# Check health
curl http://localhost:5000/api/health

# Test chat
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is diabetes?"}'
```

## 🌐 URLs

- **App:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health
- **API Endpoint:** http://localhost:5000/api/chat

## 📊 Tech Stack

- **Backend:** Python, Flask
- **LLM:** Groq (Llama 3.1 70B)
- **Embeddings:** sentence-transformers
- **Vector DB:** ChromaDB
- **Frontend:** HTML, CSS, JavaScript

## 🐛 Troubleshooting

### App won't start?
```bash
# Check if venv is activated (you should see (venv) in prompt)
# If not:
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Then reinstall:
pip install -r requirements.txt
```

### "Vector store is empty"?
```bash
python initialize_kb.py
```

### "Groq API error"?
- Check `.env` has correct API key
- No spaces: `GROQ_API_KEY=gsk_abc123`
- Get new key at console.groq.com

### Port 5000 in use?
```bash
# Use different port
set PORT=8000  # Windows
export PORT=8000  # Mac/Linux
python app.py
```

## 📚 Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup
- [README.md](README.md) - Full documentation
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deploy to cloud
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - Technical details

## ✅ Checklist Before Running

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file created
- [ ] Groq API key added to `.env`
- [ ] Knowledge base initialized
- [ ] Ready to run!

## 🎯 Sample Queries

Try these in the app:

1. "What are the symptoms of diabetes?"
2. "Explain how antibiotics work"
3. "What is cardiovascular disease?"
4. "Tell me about the immune system"
5. "What are the types of cancer?"

## 🚀 Deploy to Cloud (Free)

### Render (Recommended)
1. Push to GitHub
2. Sign up at [render.com](https://render.com)
3. Create new Web Service
4. Connect GitHub repo
5. Add environment variables
6. Deploy!

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for details.

## 📞 Need Help?

1. Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
2. Read error messages carefully
3. Ensure all steps completed
4. Check Python version: `python --version`
5. Verify venv activated: look for `(venv)` in prompt

## 💡 Pro Tips

1. Keep venv activated while working
2. Run initialization once only
3. First run downloads models (takes time)
4. Subsequent runs are fast
5. Press CTRL+C to stop server

## 📈 Project Stats

- **Medical Topics:** 50+
- **Technologies:** 10+
- **Lines of Code:** 3,000+
- **API Endpoints:** 5
- **Documentation Pages:** 5

---

**Quick Help:** If stuck, just run `quick_start.bat` (Windows) or `./quick_start.sh` (Mac/Linux)!

**Get API Key:** [https://console.groq.com](https://console.groq.com) (FREE)

**Access App:** [http://localhost:5000](http://localhost:5000)

---

Happy coding! 🌿

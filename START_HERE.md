# 🌿 JUNIPER - START HERE

## Welcome to Your Professional RAG Chatbot Project!

This is a **production-level** medical research assistant using cutting-edge AI technology (RAG + LLM).

---

## ⚡ FASTEST WAY TO START (30 seconds)

### Windows Users:
**Just double-click this file:** `quick_start.bat`

### Mac/Linux Users:
**Run:** `./quick_start.sh`

That's it! The script will:
1. Create virtual environment
2. Install all dependencies
3. Ask for your Groq API key
4. Initialize the knowledge base
5. Start the application

---

## 🎯 If Quick Start Doesn't Work

### Step 1: Get Free API Key (2 minutes)

1. Visit: **https://console.groq.com**
2. Sign up (free, no credit card)
3. Click "API Keys" → "Create API Key"
4. Copy the key (starts with `gsk_...`)

### Step 2: Manual Setup (5 minutes)

Open terminal/command prompt and run these commands:

```bash
# 1. Go to project folder
cd c:\Users\defaultuser0\OneDrive\Desktop\JUNIPER-RAG

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
# WINDOWS:
venv\Scripts\activate

# MAC/LINUX:
source venv/bin/activate

# 4. Install dependencies (takes 3-5 minutes)
pip install -r requirements.txt

# 5. Create .env file
# WINDOWS:
copy .env.example .env

# MAC/LINUX:
cp .env.example .env

# 6. Open .env in notepad/text editor
notepad .env  # Windows
nano .env     # Mac/Linux

# 7. Add your API key:
GROQ_API_KEY=gsk_your_actual_key_here

# 8. Initialize knowledge base (takes 2-5 minutes)
python initialize_kb.py

# 9. Start the app!
python app.py
```

### Step 3: Access Juniper

Open browser and go to: **http://localhost:5000**

You should see the Juniper interface! 🎉

---

## 📚 What You Get

### Medical Knowledge Base
50+ comprehensive topics including:
- Cardiovascular diseases
- Diabetes & endocrine
- Respiratory diseases
- Infectious diseases
- Neurological disorders
- Cancer types
- Mental health
- Pharmacology
- And much more!

### Advanced Technology
- **RAG Architecture** (Retrieval-Augmented Generation)
- **Vector Database** (ChromaDB)
- **Semantic Search** (sentence-transformers)
- **Large Language Model** (Llama 3.1 70B via Groq)
- **Modern UI** (Responsive, professional design)

### Features
✅ Real-time medical information
✅ Conversation history
✅ Source attribution
✅ Context-aware responses
✅ Dark/light themes
✅ Mobile-friendly
✅ 100% free to run

---

## 🎓 Perfect for University Projects

This project demonstrates:
- Advanced AI/ML concepts
- Full-stack development
- Production-ready code
- Professional documentation
- Real-world deployment

---

## 📖 Documentation

- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick commands & tips
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[README.md](README.md)** - Full project documentation
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical details
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Deploy to internet

---

## ❓ Common Issues & Solutions

### "python: command not found"
**Solution:** Install Python from python.org

### "pip: command not found"
**Solution:** Python comes with pip. Reinstall Python.

### Can't activate virtual environment
**Windows:** Run `venv\Scripts\activate.bat`
**Mac/Linux:** Run `source venv/bin/activate`

### "Vector store is empty"
**Solution:** Run `python initialize_kb.py`

### "Groq API error"
**Solutions:**
1. Check `.env` file has correct key
2. Make sure no spaces: `GROQ_API_KEY=gsk_abc`
3. Get new key at console.groq.com

### Port 5000 already in use
**Solution:**
```bash
set PORT=8000     # Windows
export PORT=8000  # Mac/Linux
python app.py
```

---

## 🚀 Deploy to Internet (FREE)

Want to show your project to the world?

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/juniper.git
   git push -u origin main
   ```

2. **Deploy to Render (Free):**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Create new Web Service
   - Connect your repository
   - Add environment variables
   - Deploy!

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

---

## 🎯 Try These Sample Queries

Once the app is running, try:

1. "What are the symptoms of diabetes?"
2. "Explain how antibiotics work"
3. "What is cardiovascular disease?"
4. "Tell me about the immune system"
5. "What are the treatments for asthma?"

---

## 📊 Project Statistics

- **Medical Topics:** 50+
- **Lines of Code:** 3,000+
- **Technologies Used:** 10+
- **Supported Platforms:** Windows, Mac, Linux, Web
- **Cost to Run:** $0 (100% free)

---

## ✅ Success Checklist

Before starting, make sure you have:

- [ ] Python 3.8 or higher installed
- [ ] Internet connection
- [ ] Groq API key (free from console.groq.com)
- [ ] 10-15 minutes for first-time setup
- [ ] A code editor (optional, but helpful)

---

## 💡 What Makes This Special?

### Unlike Tutorial Projects:
✅ **Production-ready code** (not a toy example)
✅ **Complete solution** (frontend + backend)
✅ **Advanced AI** (RAG, vector search, LLM)
✅ **Professional UI** (modern, responsive)
✅ **Comprehensive docs** (5+ documentation files)
✅ **Deployable** (works on cloud platforms)
✅ **100% free** (no paid services needed)

### Similar to Projects Like Yako:
✅ Modern web interface
✅ Real-time chat experience
✅ Professional design
✅ Production deployment ready

### But Enhanced With:
✅ **RAG architecture** (not just simple LLM calls)
✅ **Vector database** (semantic search)
✅ **Embedded knowledge** (self-contained)
✅ **Medical domain** (academic relevance)
✅ **Python backend** (as you requested)

---

## 🎓 Academic Presentation Tips

When presenting this project:

1. **Emphasize the RAG architecture** - explain how it differs from simple chatbots
2. **Demonstrate the semantic search** - show how it finds relevant medical info
3. **Highlight the self-contained nature** - no external files needed
4. **Show the professional UI** - responsive, modern design
5. **Explain the tech stack** - integration of multiple technologies
6. **Demonstrate deployment** - it works on the internet, not just locally

---

## 🌟 Next Steps

After getting it running:

1. **Test thoroughly** - try various medical queries
2. **Customize** - add more medical topics if desired
3. **Deploy** - put it on the internet
4. **Document** - take screenshots for your presentation
5. **Share** - put it on GitHub with good README

---

## 📞 Need More Help?

1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick commands
2. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed steps
3. Look at error messages - they usually tell you what's wrong
4. Make sure Python 3.8+ is installed: `python --version`
5. Verify virtual environment is activated (look for `(venv)` in terminal)

---

## 🎉 You're All Set!

**Time to build something amazing!**

1. Run the quick start script
2. Get your API key
3. Start the app
4. Test it out
5. Deploy to the internet
6. Show it to your professor! 🎓

---

**Remember:** This is a production-level project. Take your time to understand each component. It's designed to impress!

**Good luck with your university project! 🌿**

---

## 📧 Quick Links

- **Get API Key:** https://console.groq.com
- **Project Type Reference:** https://github.com/Talhahax/Yako
- **Deploy (Free):** https://render.com
- **Local Access:** http://localhost:5000

---

**Built with ❤️ for academic excellence and real-world impact!**

# Deployment Guide

This guide covers deploying Juniper to various platforms.

## 🌐 Deployment Options

### Option 1: Render (Recommended - Completely Free)

Render offers free hosting for Python apps with persistent storage.

#### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/juniper-rag.git
   git push -u origin main
   ```

2. **Sign up for Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

3. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** juniper-medical-assistant
     - **Environment:** Python
     - **Build Command:** `pip install -r requirements.txt && python initialize_kb.py`
     - **Start Command:** `gunicorn app:app`
     - **Plan:** Free

4. **Set Environment Variables**
   In Render dashboard, add:
   - `GROQ_API_KEY`: your_api_key
   - `FLASK_ENV`: production
   - `SECRET_KEY`: generate_random_string

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build and initialization (5-10 minutes)
   - Your app will be live at `https://juniper-medical-assistant.onrender.com`

**Note:** Free tier may spin down after inactivity. First request after idle may take 30-60 seconds.

---

### Option 2: Railway

Railway offers $5 free credit monthly.

#### Steps:

1. **Push to GitHub** (if not already done)

2. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Deploy from GitHub**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway auto-detects Python

4. **Add Environment Variables**
   - Go to Variables tab
   - Add: `GROQ_API_KEY`, `FLASK_ENV=production`, `SECRET_KEY`

5. **Configure Build**
   - Build Command: `pip install -r requirements.txt && python initialize_kb.py`
   - Start Command: `gunicorn app:app`

6. **Generate Domain**
   - Go to Settings → Generate Domain
   - Your app will be live!

---

### Option 3: Vercel (Serverless)

**Warning:** ChromaDB requires persistent storage. Vercel is serverless and may not work well for this use case. Better for frontend-only or stateless APIs.

If you still want to try:

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

3. Set environment variables:
   ```bash
   vercel env add GROQ_API_KEY
   vercel env add FLASK_ENV
   ```

4. Redeploy:
   ```bash
   vercel --prod
   ```

**Note:** You may need to modify the app to use a remote vector store.

---

### Option 4: Heroku

Heroku retired free tier but offers student credits through GitHub Student Developer Pack.

#### Steps:

1. **Create `Procfile`** (already included):
   ```
   web: gunicorn app:app
   ```

2. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

3. **Create Heroku app**:
   ```bash
   heroku create juniper-medical-assistant
   ```

4. **Set environment variables**:
   ```bash
   heroku config:set GROQ_API_KEY=your_key
   heroku config:set FLASK_ENV=production
   heroku config:set SECRET_KEY=random_string
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

6. **Initialize knowledge base**:
   ```bash
   heroku run python initialize_kb.py
   ```

---

### Option 5: Local Network Deployment

Deploy on your local network (accessible to devices on same WiFi).

1. **Find your local IP**:
   ```bash
   # Windows
   ipconfig
   # Look for IPv4 Address (e.g., 192.168.1.100)

   # Mac/Linux
   ifconfig
   # Look for inet address
   ```

2. **Run with host binding**:
   ```bash
   python app.py
   ```
   App runs on `0.0.0.0:5000` by default

3. **Access from other devices**:
   ```
   http://192.168.1.100:5000
   ```

---

## 🔧 Production Optimizations

### 1. Use Production WSGI Server

Replace Flask's development server with Gunicorn (already in requirements.txt):

```bash
gunicorn --workers 4 --bind 0.0.0.0:5000 app:app
```

### 2. Enable HTTPS

Most platforms (Render, Railway, Vercel) provide HTTPS automatically.

For custom domains, use Let's Encrypt or platform's SSL.

### 3. Set Up Monitoring

**Render:** Built-in metrics dashboard

**Custom:** Use services like:
- [UptimeRobot](https://uptimerobot.com) (free)
- [Sentry](https://sentry.io) for error tracking

### 4. Database Backup

Backup your ChromaDB data folder:
```bash
tar -czf chroma_backup.tar.gz data/chroma_db/
```

Store backups in cloud storage (Google Drive, Dropbox, etc.)

### 5. Rate Limiting

Add rate limiting to prevent abuse:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)
```

---

## 🌍 Custom Domain Setup

### For Render:

1. Buy domain (Namecheap, GoDaddy, etc.)
2. In Render dashboard: Settings → Custom Domain
3. Add your domain
4. Update DNS records as instructed

### For Railway:

1. Settings → Domains → Add Custom Domain
2. Follow DNS configuration instructions

---

## 📊 Performance Tips

1. **Caching:** Implement response caching for common queries
2. **CDN:** Use Cloudflare for static assets
3. **Optimize Embeddings:** Pre-compute and cache frequent queries
4. **Database:** Consider Redis for session management
5. **Load Balancing:** Use multiple instances for high traffic

---

## 🔒 Security Checklist

- [ ] Environment variables set (not hardcoded)
- [ ] `.env` file in `.gitignore`
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] Regular dependency updates
- [ ] API keys rotated periodically

---

## 📱 Testing Your Deployment

After deployment, test:

1. **Health endpoint:**
   ```bash
   curl https://your-app.onrender.com/api/health
   ```

2. **Chat endpoint:**
   ```bash
   curl -X POST https://your-app.onrender.com/api/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is diabetes?"}'
   ```

3. **Load test** with multiple concurrent requests

4. **Mobile responsiveness** on different devices

---

## 🎯 Deployment Checklist

Before deploying:

- [ ] All dependencies in `requirements.txt`
- [ ] Environment variables documented
- [ ] `.gitignore` includes sensitive files
- [ ] README.md updated
- [ ] Knowledge base initialized
- [ ] Local testing passed
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Security measures in place

---

## 💰 Cost Comparison

| Platform | Free Tier | Pros | Cons |
|----------|-----------|------|------|
| **Render** | ✅ Forever free | Easy setup, persistent storage | Sleeps after inactivity |
| **Railway** | $5/month credit | Fast, good DX | Limited free credit |
| **Vercel** | ✅ Free | Excellent for frontend | Not ideal for stateful apps |
| **Heroku** | ❌ (paid only) | Mature platform | No free tier |

**Recommendation:** Start with **Render** for free hosting, upgrade to **Railway** if you need better performance.

---

## 🚨 Common Deployment Issues

### Issue: App crashes on startup

**Check:**
- Build logs for errors
- All dependencies installed
- Environment variables set
- Python version compatibility

### Issue: ChromaDB errors

**Solution:**
- Ensure persistent storage is configured
- Run initialization script in build command
- Check file system permissions

### Issue: Slow responses

**Solutions:**
- Use faster embedding model
- Implement caching
- Optimize vector search parameters
- Upgrade to paid tier for more resources

---

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Test locally first
4. Check community forums (Render Community, Railway Discord)

---

**Happy Deploying! 🚀**

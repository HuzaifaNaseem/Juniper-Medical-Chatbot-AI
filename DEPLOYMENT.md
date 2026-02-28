# DigitalOcean Deployment Guide for Juniper

This guide will walk you through deploying Juniper Medical Research Assistant on DigitalOcean.

## Prerequisites

- DigitalOcean account with $12/month droplet subscription
- GitHub repository with your code
- Groq API key (free at https://console.groq.com)

## Deployment Options

### Option 1: DigitalOcean App Platform (Recommended - Easy)

This is the easiest method with automatic deployments from GitHub.

#### Step 1: Create App

1. Log into DigitalOcean
2. Go to **Apps** in the left menu
3. Click **Create App**
4. Select **GitHub** as source
5. Authorize DigitalOcean to access your GitHub
6. Select your Juniper repository
7. Click **Next**

#### Step 2: Configure App

1. **Resource Type**: Web Service
2. **Build Command**: Leave default or use:
   ```
   pip install -r requirements.txt
   ```

3. **Run Command**:
   ```
   bash start.sh
   ```

4. **HTTP Port**: 8080

5. Click **Next**

#### Step 3: Set Environment Variables

Click **Edit** next to Environment Variables and add:

```
FLASK_ENV=production
SECRET_KEY=<generate-a-random-secret-key>
GROQ_API_KEY=<your-groq-api-key-here>
CORS_ORIGINS=*
PORT=8080
```

To generate a secure SECRET_KEY, run:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Step 4: Choose Plan

1. Select **Basic** plan ($12/month)
2. Choose your preferred datacenter region
3. Review and click **Create Resources**

#### Step 5: Wait for Deployment

- DigitalOcean will build and deploy your app
- This may take 5-10 minutes on first deployment
- Once complete, you'll see a URL like `https://your-app-name.ondigitalocean.app`

#### Step 6: Verify Deployment

1. Visit your app URL
2. Check the health endpoint: `https://your-app-name.ondigitalocean.app/api/health`
3. Try asking a medical question in the chat interface

---

### Option 2: Droplet with Ubuntu (Advanced)

For more control, deploy on a DigitalOcean Droplet.

#### Step 1: Create Droplet

1. Go to **Droplets** > **Create Droplet**
2. Choose **Ubuntu 22.04 LTS**
3. Select **Basic** plan ($12/month)
4. Choose datacenter region
5. Add SSH key or password
6. Click **Create Droplet**

#### Step 2: SSH into Droplet

```bash
ssh root@your-droplet-ip
```

#### Step 3: Install Dependencies

```bash
# Update system
apt update && apt upgrade -y

# Install Python and required packages
apt install -y python3 python3-pip python3-venv git nginx

# Install supervisor for process management
apt install -y supervisor
```

#### Step 4: Clone Repository

```bash
# Create app directory
mkdir -p /var/www
cd /var/www

# Clone your repository
git clone https://github.com/yourusername/juniper-rag.git juniper
cd juniper

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

#### Step 5: Configure Environment

```bash
# Create .env file
nano .env
```

Add the following content:
```
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key
GROQ_API_KEY=your-groq-api-key
CORS_ORIGINS=*
PORT=8080
```

Save and exit (Ctrl+X, Y, Enter)

#### Step 6: Initialize Knowledge Base

```bash
# Make sure virtual environment is activated
source /var/www/juniper/venv/bin/activate

# Initialize the knowledge base
python initialize_kb.py
```

#### Step 7: Configure Supervisor

Create supervisor config:
```bash
nano /etc/supervisor/conf.d/juniper.conf
```

Add this configuration:
```ini
[program:juniper]
directory=/var/www/juniper
command=/var/www/juniper/venv/bin/gunicorn wsgi:application --bind 0.0.0.0:8080 --workers 4 --worker-class gevent --timeout 120
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/juniper/err.log
stdout_logfile=/var/log/juniper/out.log
environment=PATH="/var/www/juniper/venv/bin"
```

Create log directory:
```bash
mkdir -p /var/log/juniper
```

Update and start supervisor:
```bash
supervisorctl reread
supervisorctl update
supervisorctl start juniper
```

Check status:
```bash
supervisorctl status juniper
```

#### Step 8: Configure Nginx (Optional - for custom domain)

```bash
nano /etc/nginx/sites-available/juniper
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # Change this to your domain

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeout for AI processing
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/juniper /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### Step 9: Configure Firewall

```bash
# Allow SSH, HTTP, and HTTPS
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

#### Step 10: Access Your App

- Direct access: `http://your-droplet-ip:8080`
- With Nginx: `http://your-domain.com`

---

## Post-Deployment

### Monitoring

Check application logs:

**App Platform:**
- Go to your app in DigitalOcean dashboard
- Click **Runtime Logs**

**Droplet:**
```bash
# View live logs
tail -f /var/log/juniper/out.log

# View error logs
tail -f /var/log/juniper/err.log
```

### Updating Your App

**App Platform:**
- Push changes to GitHub
- DigitalOcean auto-deploys from main branch

**Droplet:**
```bash
cd /var/www/juniper
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
supervisorctl restart juniper
```

### Health Checks

Monitor your app:
- Health endpoint: `/api/health`
- Stats endpoint: `/api/stats`

Set up DigitalOcean monitoring alerts for:
- CPU usage > 80%
- Memory usage > 80%
- Disk usage > 80%

---

## Troubleshooting

### Issue: App won't start

**Check logs:**
```bash
# App Platform: View Runtime Logs in dashboard
# Droplet:
tail -50 /var/log/juniper/err.log
```

**Common causes:**
- Missing GROQ_API_KEY
- Knowledge base not initialized
- Port already in use

**Solution:**
- Verify environment variables
- Run `python initialize_kb.py`
- Change PORT in environment variables

### Issue: Out of memory

**Solution:** Reduce number of workers in [start.sh](start.sh:26):
```bash
--workers 2  # Instead of 4
```

### Issue: Slow responses

**Causes:**
- Heavy traffic
- ChromaDB performance
- Groq API latency

**Solutions:**
- Upgrade to larger droplet
- Add Redis caching
- Implement request queuing

### Issue: Knowledge base initialization fails

**Check:**
- Sufficient disk space
- Python dependencies installed
- Sentence transformers can download models

**Solution:**
```bash
# Manually download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

---

## Security Best Practices

1. **Environment Variables:** Never commit `.env` to Git
2. **SECRET_KEY:** Use a strong, randomly generated key
3. **API Keys:** Rotate keys periodically
4. **HTTPS:** Use SSL certificate (Nginx + Let's Encrypt)
5. **Firewall:** Only allow necessary ports
6. **Updates:** Keep system and dependencies updated

---

## Custom Domain Setup

1. Buy domain from registrar (Namecheap, GoDaddy, etc.)
2. Add domain to DigitalOcean:
   - **App Platform:** Go to Settings > Domains
   - **Droplet:** Configure DNS A record to point to droplet IP
3. Configure SSL certificate (App Platform does this automatically)

---

## Scaling

As your usage grows:

1. **Vertical Scaling:** Upgrade to larger droplet/plan
2. **Horizontal Scaling:** Use load balancer with multiple app instances
3. **Database:** Move ChromaDB to persistent volume or external service
4. **Caching:** Add Redis for response caching
5. **CDN:** Use DigitalOcean Spaces for static assets

---

## Cost Optimization

- **Basic $12/month:** Handles ~1000-2000 requests/day
- **Pro $24/month:** Handles ~5000-10000 requests/day
- Monitor usage and scale as needed
- Groq API is free (no additional cost)

---

## Support

If you encounter issues:

1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Contact: huzaifakhan654916@gmail.com

---

## Next Steps

After successful deployment:

1. Test all endpoints thoroughly
2. Set up monitoring and alerts
3. Configure custom domain (optional)
4. Implement backup strategy
5. Document any customizations
6. Share with users!

Congratulations! Your Juniper Medical Research Assistant is now live on DigitalOcean! 🎉

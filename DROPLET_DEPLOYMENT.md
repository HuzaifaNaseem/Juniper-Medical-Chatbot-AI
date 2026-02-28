# Quick Droplet Deployment Guide

Your Droplet Details:
- **Name**: Juniper-Medical-Chatbot
- **IP**: 139.59.41.114
- **OS**: Ubuntu 24.04 LTS

## Method 1: Automated Deployment (Easiest)

### Step 1: SSH into your Droplet

Open your terminal (PowerShell/CMD on Windows) and connect:

```bash
ssh root@139.59.41.114
```

You'll be prompted for your password (the one DigitalOcean emailed you).

### Step 2: Download and Run Deployment Script

Once connected, run these commands:

```bash
# Download the deployment script
curl -o deploy.sh https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/master/Juniper-Medical-Chatbot-AI--master/deploy_droplet.sh

# Make it executable
chmod +x deploy.sh

# Run the script
./deploy.sh
```

The script will:
- Update system packages
- Install Python, Git, Nginx, Supervisor
- Clone your GitHub repository
- Set up virtual environment
- Ask for your Groq API key
- Initialize the knowledge base
- Configure and start the application

---

## Method 2: Manual Deployment (Step by Step)

If you prefer to do it manually, follow these steps:

### Step 1: SSH into Droplet

```bash
ssh root@139.59.41.114
```

### Step 2: Update System

```bash
apt update && apt upgrade -y
```

### Step 3: Install Dependencies

```bash
apt install -y python3 python3-pip python3-venv git nginx supervisor
```

### Step 4: Clone Repository

```bash
# Create app directory
mkdir -p /var/www/juniper
cd /var/www/juniper

# Clone your repository (replace with your GitHub URL)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git .

# If nested directory exists, navigate into it
cd Juniper-Medical-Chatbot-AI--master
```

### Step 5: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Create .env File

```bash
nano .env
```

Add this content (replace with your actual keys):

```
FLASK_ENV=production
SECRET_KEY=your-generated-secret-key-here
GROQ_API_KEY=your-groq-api-key-here
CORS_ORIGINS=*
PORT=8080
```

**To generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Save and exit: `Ctrl+X`, then `Y`, then `Enter`

### Step 7: Initialize Knowledge Base

```bash
python3 initialize_kb.py
```

Wait for it to complete (may take a few minutes).

### Step 8: Configure Supervisor

Create supervisor config:

```bash
nano /etc/supervisor/conf.d/juniper.conf
```

Add this content (adjust paths if needed):

```ini
[program:juniper]
directory=/var/www/juniper/Juniper-Medical-Chatbot-AI--master
command=/var/www/juniper/Juniper-Medical-Chatbot-AI--master/venv/bin/gunicorn wsgi:application --bind 0.0.0.0:8080 --workers 4 --worker-class gevent --timeout 120 --log-level info
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/juniper/err.log
stdout_logfile=/var/log/juniper/out.log
environment=PATH="/var/www/juniper/Juniper-Medical-Chatbot-AI--master/venv/bin"
```

Save and exit.

### Step 9: Create Log Directory

```bash
mkdir -p /var/log/juniper
```

### Step 10: Start Application

```bash
supervisorctl reread
supervisorctl update
supervisorctl start juniper
```

### Step 11: Check Status

```bash
supervisorctl status juniper
```

Should show: `juniper    RUNNING`

### Step 12: Configure Firewall

```bash
ufw allow OpenSSH
ufw allow 8080
ufw enable
```

Type `y` when prompted.

---

## Accessing Your Application

Once deployed, access your app at:

**http://139.59.41.114:8080**

Test the health endpoint:

**http://139.59.41.114:8080/api/health**

---

## Useful Commands

```bash
# Check app status
supervisorctl status juniper

# Restart app
supervisorctl restart juniper

# Stop app
supervisorctl stop juniper

# View live logs
tail -f /var/log/juniper/out.log

# View error logs
tail -f /var/log/juniper/err.log

# Update app (after pushing changes to GitHub)
cd /var/www/juniper/Juniper-Medical-Chatbot-AI--master
git pull origin master
source venv/bin/activate
pip install -r requirements.txt
supervisorctl restart juniper
```

---

## Optional: Set Up Nginx Reverse Proxy

To access your app on port 80 (standard HTTP):

### Step 1: Configure Nginx

```bash
nano /etc/nginx/sites-available/juniper
```

Add:

```nginx
server {
    listen 80;
    server_name 139.59.41.114;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 300s;
    }
}
```

### Step 2: Enable Site

```bash
ln -s /etc/nginx/sites-available/juniper /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Step 3: Update Firewall

```bash
ufw allow 'Nginx Full'
```

Now access your app at: **http://139.59.41.114** (without port 8080)

---

## Troubleshooting

### App Won't Start

Check logs:
```bash
tail -50 /var/log/juniper/err.log
```

Common issues:
- Missing GROQ_API_KEY in .env
- Knowledge base not initialized
- Wrong directory paths in supervisor config

### Out of Memory

Reduce workers in supervisor config to `--workers 2`

### Port Already in Use

Check what's using port 8080:
```bash
lsof -i :8080
```

Kill the process or use a different port.

---

## Need Help?

If you encounter any issues, let me know and I'll help you troubleshoot!

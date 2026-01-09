#!/bin/bash
# Automated Deployment Script for DigitalOcean Droplet
# Run this script on your droplet after SSH

set -e  # Exit on error

echo "================================================"
echo "Juniper Medical Chatbot - Droplet Deployment"
echo "================================================"

# Update system
echo ""
echo "[1/8] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo ""
echo "[2/8] Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor

# Create application directory
echo ""
echo "[3/8] Setting up application directory..."
sudo mkdir -p /var/www/juniper
cd /var/www/juniper

# Clone repository (you'll need to enter your GitHub URL)
echo ""
echo "[4/8] Cloning repository..."
echo "Please provide your GitHub repository URL (e.g., https://github.com/yourusername/juniper-rag.git):"
read REPO_URL

if [ -d ".git" ]; then
    echo "Repository already exists, pulling latest changes..."
    sudo git pull origin master
else
    sudo git clone "$REPO_URL" .
fi

# Navigate to correct directory if nested
if [ -d "Juniper-Medical-Chatbot-AI--master" ]; then
    cd Juniper-Medical-Chatbot-AI--master
fi

# Create virtual environment
echo ""
echo "[5/8] Creating virtual environment and installing dependencies..."
sudo python3 -m venv venv
sudo chown -R $USER:$USER venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Setup environment variables
echo ""
echo "[6/8] Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file..."
    echo "Please enter your Groq API Key:"
    read GROQ_KEY

    echo "Generating SECRET_KEY..."
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

    cat > .env << EOF
FLASK_ENV=production
SECRET_KEY=$SECRET_KEY
GROQ_API_KEY=$GROQ_KEY
CORS_ORIGINS=*
PORT=8080
EOF
    echo ".env file created successfully"
else
    echo ".env file already exists"
fi

# Initialize knowledge base
echo ""
echo "[7/8] Initializing knowledge base..."
python3 initialize_kb.py

# Create log directory
sudo mkdir -p /var/log/juniper
sudo chown -R $USER:$USER /var/log/juniper

# Configure Supervisor
echo ""
echo "[8/8] Configuring Supervisor..."
APP_DIR=$(pwd)
VENV_DIR="$APP_DIR/venv"

sudo tee /etc/supervisor/conf.d/juniper.conf > /dev/null <<EOF
[program:juniper]
directory=$APP_DIR
command=$VENV_DIR/bin/gunicorn wsgi:application --bind 0.0.0.0:8080 --workers 4 --worker-class gevent --timeout 120 --log-level info
user=$USER
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/juniper/err.log
stdout_logfile=/var/log/juniper/out.log
environment=PATH="$VENV_DIR/bin"
EOF

# Update and start supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start juniper

# Wait a moment for app to start
sleep 3

# Check status
echo ""
echo "================================================"
echo "Checking application status..."
sudo supervisorctl status juniper

echo ""
echo "================================================"
echo "DEPLOYMENT COMPLETE!"
echo "================================================"
echo ""
echo "Your application should now be running!"
echo ""
echo "Access your app at:"
echo "  http://$(curl -s ifconfig.me):8080"
echo ""
echo "Useful commands:"
echo "  sudo supervisorctl status juniper    # Check status"
echo "  sudo supervisorctl restart juniper   # Restart app"
echo "  tail -f /var/log/juniper/out.log     # View logs"
echo "  tail -f /var/log/juniper/err.log     # View errors"
echo ""
echo "Next steps:"
echo "  1. Configure firewall to allow port 8080"
echo "  2. Optionally set up Nginx as reverse proxy"
echo "  3. Optionally configure SSL certificate"
echo ""
echo "================================================"

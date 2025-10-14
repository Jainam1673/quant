# Deployment Guide

## Overview

This guide covers deploying the Quant Trading Platform to production environments.

## Prerequisites

- Linux server with Python 3.13+
- Domain name (optional, for HTTPS)
- Reverse proxy (nginx or Caddy recommended)
- Process manager (systemd, supervisor, or PM2)

---

## Deployment Options

### Option 1: Self-Hosted Server

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.13 python3.13-venv nginx certbot python3-certbot-nginx

# Create application user
sudo useradd -m -s /bin/bash quantapp
sudo su - quantapp
```

#### 2. Clone and Setup

```bash
# Clone repository
git clone https://github.com/yourusername/quant.git
cd quant

# Create virtual environment
python3.13 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
nano .env  # Edit configuration
```

#### 3. Build Application

```bash
# Export static frontend
reflex export --frontend-only

# Or build with backend
reflex export
```

#### 4. Configure Nginx

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/quant
```

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /home/quantapp/quant/.web/_static;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket for Reflex
    location /_event {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    client_max_body_size 50M;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/quant /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Setup SSL (Optional but Recommended)

```bash
sudo certbot --nginx -d yourdomain.com
```

#### 6. Create Systemd Service

```bash
sudo nano /etc/systemd/system/quant.service
```

```ini
[Unit]
Description=Quant Trading Platform
After=network.target

[Service]
Type=simple
User=quantapp
WorkingDirectory=/home/quantapp/quant
Environment="PATH=/home/quantapp/quant/.venv/bin"
Environment="APP_ENV=production"
ExecStart=/home/quantapp/quant/.venv/bin/reflex run --env prod --backend-only --backend-port 8000
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable quant
sudo systemctl start quant
sudo systemctl status quant
```

---

### Option 2: Docker Deployment

#### 1. Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for Reflex
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Build frontend
RUN reflex export --frontend-only

# Expose ports
EXPOSE 3000 8000

# Run application
CMD ["reflex", "run", "--env", "prod"]
```

#### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  quant:
    build: .
    ports:
      - "3000:3000"
      - "8000:8000"
    environment:
      - APP_ENV=production
      - LOG_LEVEL=INFO
      - DB_PATH=/data/quant.duckdb
    volumes:
      - quant-data:/data
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - quant
    restart: unless-stopped

volumes:
  quant-data:
```

#### 3. Deploy

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f quant

# Stop
docker-compose down
```

---

### Option 3: Cloud Platform (Heroku, Railway, Render)

#### Heroku Deployment

1. **Create Procfile**

```
web: reflex run --env prod --backend-port $PORT
```

2. **Create runtime.txt**

```
python-3.13.0
```

3. **Deploy**

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set APP_ENV=production
heroku config:set LOG_LEVEL=INFO

# Deploy
git push heroku main

# Open app
heroku open
```

#### Railway Deployment

1. Connect GitHub repository
2. Add environment variables
3. Set start command: `reflex run --env prod`
4. Deploy automatically on push

#### Render Deployment

1. **render.yaml**

```yaml
services:
  - type: web
    name: quant-platform
    env: python
    buildCommand: pip install -r requirements.txt && reflex export
    startCommand: reflex run --env prod
    envVars:
      - key: APP_ENV
        value: production
      - key: PYTHON_VERSION
        value: 3.13.0
```

2. Connect repository and deploy

---

## Environment Configuration

### Production Environment Variables

```bash
# .env (production)
APP_ENV=production
LOG_LEVEL=INFO
DB_PATH=/var/lib/quant/quant.duckdb

# Security
SECRET_KEY=your-secret-key-here

# Performance
REFLEX_BACKEND_PORT=8000
REFLEX_FRONTEND_PORT=3000

# Database
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# External APIs (if needed)
ALPHA_VANTAGE_KEY=your-key
POLYGON_API_KEY=your-key
```

---

## Performance Optimization

### 1. Database Optimization

```python
# Use connection pooling
from quant.data import Database

db = Database(
    db_path="/path/to/quant.duckdb",
    read_only=False,
    threads=4
)
```

### 2. Caching

```bash
# Install Redis for caching
sudo apt install redis-server

# Enable in rxconfig.py
redis_url = "redis://localhost:6379"
```

### 3. Frontend Optimization

```bash
# Enable compression in nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
gzip_min_length 1000;

# Enable caching
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 4. Process Management

```bash
# Increase worker processes
gunicorn --workers 4 --threads 2 --bind 0.0.0.0:8000 quant:app
```

---

## Monitoring & Logging

### 1. Application Logs

```bash
# View systemd logs
sudo journalctl -u quant -f

# View application logs
tail -f /var/log/quant/app.log
```

### 2. Performance Monitoring

```bash
# Install monitoring tools
pip install prometheus-client
pip install sentry-sdk

# Add to application
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    environment="production"
)
```

### 3. Health Checks

```python
# Add health endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

---

## Backup Strategy

### 1. Database Backup

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/quant"
DB_PATH="/var/lib/quant/quant.duckdb"

mkdir -p $BACKUP_DIR
cp $DB_PATH $BACKUP_DIR/quant_$DATE.duckdb
find $BACKUP_DIR -mtime +7 -delete  # Keep 7 days
```

### 2. Automated Backups

```bash
# Add to crontab
0 2 * * * /home/quantapp/backup.sh
```

---

## Security Checklist

- [ ] Use HTTPS (SSL/TLS certificate)
- [ ] Set secure environment variables
- [ ] Enable firewall (ufw/iptables)
- [ ] Keep dependencies updated
- [ ] Use strong database passwords
- [ ] Enable rate limiting
- [ ] Implement input validation
- [ ] Regular security audits
- [ ] Monitor logs for suspicious activity
- [ ] Keep backups encrypted

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose scale
docker-compose up -d --scale quant=3

# Load balancer nginx config
upstream quant_backend {
    least_conn;
    server quant1:8000;
    server quant2:8000;
    server quant3:8000;
}
```

### Vertical Scaling

```bash
# Increase resources in systemd
[Service]
LimitNOFILE=65536
LimitNPROC=4096
```

---

## Troubleshooting

### Common Issues

**Port Already in Use**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

**Permission Denied**
```bash
sudo chown -R quantapp:quantapp /home/quantapp/quant
sudo chmod +x /home/quantapp/quant/.venv/bin/*
```

**Database Lock**
```bash
# Check processes
ps aux | grep python

# Remove lock if safe
rm /path/to/quant.duckdb.wal
```

**Memory Issues**
```bash
# Increase swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## Maintenance

### Updates

```bash
# Stop service
sudo systemctl stop quant

# Pull latest code
cd /home/quantapp/quant
git pull origin main

# Update dependencies
source .venv/bin/activate
pip install -r requirements.txt --upgrade

# Rebuild frontend
reflex export --frontend-only

# Start service
sudo systemctl start quant
```

### Database Maintenance

```bash
# Compact database
duckdb quant.duckdb "VACUUM;"

# Check integrity
duckdb quant.duckdb "PRAGMA integrity_check;"
```

---

## Support

For deployment issues:
1. Check logs: `sudo journalctl -u quant -f`
2. Verify environment variables
3. Test database connectivity
4. Check firewall rules
5. Review nginx error logs

---

## Production Checklist

Before going live:

- [ ] SSL certificate installed
- [ ] Environment variables configured
- [ ] Database backed up
- [ ] Monitoring setup
- [ ] Logs configured
- [ ] Health checks working
- [ ] Performance tested
- [ ] Security audit completed
- [ ] Documentation updated
- [ ] Emergency procedures documented

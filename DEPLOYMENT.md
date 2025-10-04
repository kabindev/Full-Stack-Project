# 🚀 Productivity Hub - Deployment Guide

Complete guide for deploying your Productivity Hub to production.

## 🔒 Pre-Deployment Security Checklist

### 1. Update Secret Key
In `app.py`, change:
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
```

To generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### 2. Disable Debug Mode
```python
if __name__ == '__main__':
    app.run(debug=False)  # Set to False for production
```

### 3. Use Environment Variables
Create a `.env` file:
```env
SECRET_KEY=your-generated-secret-key
DATABASE_URL=sqlite:///productivity.db
FLASK_ENV=production
```

Update `app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
```

Install python-dotenv:
```bash
pip install python-dotenv
```

## 📦 Deployment Options

## Option 1: Heroku (Recommended for Beginners)

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step 1: Sign Up
- Go to [PythonAnywhere.com](https://www.pythonanywhere.com)
- Create a free account

### Step 2: Upload Files
- Go to "Files" tab
- Create directory: `/home/yourusername/productivity-hub`
- Upload all project files

### Step 3: Create Virtual Environment
Open Bash console:
```bash
cd ~/productivity-hub
mkvirtualenv --python=/usr/bin/python3.10 productivity-env
pip install -r requirements.txt
```

### Step 4: Configure Web App
- Go to "Web" tab
- Click "Add a new web app"
- Choose "Manual configuration"
- Select Python 3.10

### Step 5: Set WSGI Configuration
Edit WSGI configuration file:
```python
import sys
import os

# Add your project directory
project_home = '/home/yourusername/productivity-hub'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables
os.environ['SECRET_KEY'] = 'your-secret-key'

# Import Flask app
from app import app as application
```

### Step 6: Set Virtual Environment
In Web tab:
- Virtualenv: `/home/yourusername/.virtualenvs/productivity-env`

### Step 7: Static Files
- URL: `/static/`
- Directory: `/home/yourusername/productivity-hub/static/`

### Step 8: Reload Web App
Click "Reload" button

---

## Option 3: DigitalOcean/AWS/VPS

### Prerequisites
- Ubuntu 20.04+ server
- Domain name (optional)
- SSH access

### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Install supervisor for process management
sudo apt install supervisor -y
```

### Step 2: Clone/Upload Project
```bash
cd /var/www
sudo mkdir productivity-hub
sudo chown $USER:$USER productivity-hub
cd productivity-hub

# Upload files or clone from git
# git clone your-repository .
```

### Step 3: Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 4: Configure Gunicorn
Create `/etc/supervisor/conf.d/productivity-hub.conf`:
```ini
[program:productivity-hub]
directory=/var/www/productivity-hub
command=/var/www/productivity-hub/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/productivity-hub/err.log
stdout_logfile=/var/log/productivity-hub/out.log
environment=SECRET_KEY="your-secret-key",FLASK_ENV="production"
```

Create log directory:
```bash
sudo mkdir -p /var/log/productivity-hub
sudo chown www-data:www-data /var/log/productivity-hub
```

### Step 5: Configure Nginx
Create `/etc/nginx/sites-available/productivity-hub`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/productivity-hub/static;
        expires 30d;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/productivity-hub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 6: Start Application
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start productivity-hub
```

### Step 7: Setup SSL (Optional but Recommended)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Option 4: Docker Deployment

### Step 1: Create Dockerfile
Create `Dockerfile` in project root:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directory for database
RUN mkdir -p /app/data

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Step 2: Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Step 3: Build and Run
```bash
# Build image
docker-compose build

# Run container
docker-compose up -d

# View logs
docker-compose logs -f
```

### Step 4: Stop/Restart
```bash
# Stop
docker-compose down

# Restart
docker-compose restart
```

---

## 🗄️ Database Migration to PostgreSQL (Production)

For production, consider PostgreSQL instead of SQLite.

### Step 1: Install Dependencies
```bash
pip install psycopg2-binary
```

### Step 2: Update Configuration
```python
# For PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') or \
    'postgresql://username:password@localhost/productivity_db'
```

### Step 3: Heroku PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

### Step 4: Migrate Data
```python
# Export from SQLite
import sqlite3
import json

conn = sqlite3.connect('productivity.db')
# Export logic here

# Import to PostgreSQL
# Import logic here
```

---

## 📊 Monitoring & Maintenance

### Application Monitoring

**1. Error Logging**
Add to `app.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/productivity.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Productivity Hub startup')
```

**2. Health Check Endpoint**
```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})
```

**3. Database Backup Script**
Create `backup.sh`:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_FILE="/var/www/productivity-hub/productivity.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/backup_$DATE.db

# Keep only last 7 days
find $BACKUP_DIR -name "backup_*.db" -mtime +7 -delete

echo "Backup completed: backup_$DATE.db"
```

Setup cron:
```bash
crontab -e
# Add: 0 2 * * * /path/to/backup.sh
```

---

## 🔄 Continuous Deployment

### GitHub Actions Workflow
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

---

## 🛡️ Security Best Practices

### 1. Environment Variables
Never commit:
- Secret keys
- Database credentials
- API keys

### 2. HTTPS Only
Always use SSL in production:
```python
from flask_talisman import Talisman
Talisman(app, force_https=True)
```

### 3. Rate Limiting
```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/tasks', methods=['POST'])
@limiter.limit("10 per minute")
def create_task():
    # ... code
```

### 4. CORS (if needed)
```bash
pip install flask-cors
```

```python
from flask_cors import CORS
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

### 5. Input Validation
Always validate and sanitize user inputs.

---

## 📈 Performance Optimization

### 1. Database Indexing
```python
class Task(db.Model):
    # ... existing fields
    __table_args__ = (
        db.Index('idx_status', 'status'),
        db.Index('idx_created_at', 'created_at'),
    )
```

### 2. Caching (Flask-Caching)
```bash
pip install Flask-Caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/dashboard')
@cache.cached(timeout=60)
def get_dashboard():
    # ... code
```

### 3. Compression
```bash
pip install Flask-Compress
```

```python
from flask_compress import Compress
Compress(app)
```

---

## ✅ Post-Deployment Checklist

- [ ] Application accessible via URL
- [ ] All features working correctly
- [ ] Database initialized properly
- [ ] SSL certificate installed
- [ ] Environment variables set
- [ ] Error logging configured
- [ ] Backup system in place
- [ ] Monitoring setup
- [ ] Performance acceptable
- [ ] Security headers enabled
- [ ] CORS configured (if needed)
- [ ] Rate limiting active
- [ ] Documentation updated
- [ ] Domain pointed correctly
- [ ] Email notifications working (if added)

---

## 🆘 Troubleshooting

### Common Issues

**1. Application won't start**
```bash
# Check logs
tail -f /var/log/productivity-hub/err.log
# Or
heroku logs --tail
```

**2. Database connection error**
- Verify DATABASE_URL is correct
- Check database service is running
- Ensure migrations are applied

**3. 502 Bad Gateway**
- Check if Gunicorn is running
- Verify Nginx configuration
- Check firewall rules

**4. Slow performance**
- Enable caching
- Add database indexes
- Check server resources

**5. Scheduler not running**
- Verify APScheduler is started
- Check timezone settings
- Review scheduler logs

---

## 📞 Support & Resources

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Heroku Dev Center: https://devcenter.heroku.com/
- DigitalOcean Tutorials: https://www.digitalocean.com/community/tutorials

---

**Deployment Guide Version:** 1.0.0  
**Last Updated:** October 2025: Prepare Application

Create `Procfile`:
```
web: gunicorn app:app
```

Update `requirements.txt`:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
APScheduler==3.10.4
SQLAlchemy==2.0.23
gunicorn==21.2.0
python-dotenv==1.0.0
```

### Step 2: Initialize Git
```bash
git init
git add .
git commit -m "Initial commit"
```

### Step 3: Create Heroku App
```bash
heroku login
heroku create your-productivity-hub
```

### Step 4: Set Config Variables
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

### Step 5: Deploy
```bash
git push heroku main
```

### Step 6: Initialize Database
```bash
heroku run python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Access Your App
```bash
heroku open
```

---

## Option 2: PythonAnywhere

### Step 1
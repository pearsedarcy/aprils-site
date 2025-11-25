# Hetzner Docker Deployment Guide

This guide walks you through deploying the Wagtail site to a Hetzner Cloud server using Docker.

## Prerequisites

- A Hetzner Cloud account
- A server (CX11 or better recommended - at least 2GB RAM)
- Domain name pointed to your server's IP
- SSH access to your server

## Quick Start

### 1. Set Up Hetzner Server

```bash
# SSH into your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Docker Compose
apt install docker-compose-plugin -y

# Add your user to docker group (if not using root)
usermod -aG docker $USER
```

### 2. Clone and Configure

```bash
# Clone your repository
git clone https://github.com/pearsedarcy/aprils-site.git
cd aprils-site

# Create environment file
cp .env.example .env
nano .env  # Edit with your actual values
```

### 3. Configure Environment Variables

Edit `.env` with your production values:

```env
# Django Settings
DJANGO_SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
WAGTAILADMIN_BASE_URL=https://yourdomain.com

# Database (PostgreSQL included in docker-compose)
DATABASE_URL=postgres://wagtail:your-secure-password@db:5432/wagtail
POSTGRES_PASSWORD=your-secure-password

# Cloudinary (for media storage)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-password
```

**Important:** The `POSTGRES_PASSWORD` must match the password in `DATABASE_URL`.

### 4. Build and Deploy

```bash
# Build the Docker image
docker compose build

# Start the containers (web + PostgreSQL database)
docker compose up -d

# Check logs (both services)
docker compose logs -f

# Check just the web service
docker compose logs -f web

# Migrations run automatically on startup, but you can run manually if needed:
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser
```

**Note:** The docker-compose.yml includes PostgreSQL by default. The web service will wait for the database to be healthy before starting.

## Production Setup with Nginx and SSL

### 1. Install Nginx and Certbot

```bash
apt install nginx certbot python3-certbot-nginx -y
```

### 2. Create Nginx Configuration

Create `/etc/nginx/sites-available/wagtail`:

```nginx
upstream wagtail {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://wagtail;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /path/to/aprils-site/staticfiles/;
    }

    location /media/ {
        alias /path/to/aprils-site/media/;
    }

    client_max_body_size 100M;
}
```

### 3. Enable Site and Get SSL

```bash
# Enable the site
ln -s /etc/nginx/sites-available/wagtail /etc/nginx/sites-enabled/

# Test configuration
nginx -t

# Reload nginx
systemctl reload nginx

# Get SSL certificate
certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 4. Update Django Settings

Add your domain to `CSRF_TRUSTED_ORIGINS` in `poxed/settings/production.py`:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

---

## Production Setup with Apache (Alternative)

If your server already uses Apache (e.g., for WordPress), you can use Apache as the reverse proxy instead of Nginx.

### 1. Enable Required Apache Modules

```bash
sudo a2enmod proxy proxy_http proxy_balancer lbmethod_byrequests headers
sudo systemctl restart apache2
```

### 2. Create Apache Virtual Host

Create `/etc/apache2/sites-available/wagtail.conf`:

```apache
<VirtualHost *:80>
    ServerName stage.yourdomain.com

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    RequestHeader set X-Forwarded-Proto "http"
    RequestHeader set X-Forwarded-For "%{REMOTE_ADDR}s"

    ErrorLog ${APACHE_LOG_DIR}/wagtail_error.log
    CustomLog ${APACHE_LOG_DIR}/wagtail_access.log combined
</VirtualHost>
```

### 3. Enable Site and Get SSL

```bash
# Enable the site
sudo a2ensite wagtail.conf

# Test configuration
sudo apache2ctl configtest

# Reload Apache
sudo systemctl reload apache2

# Get SSL certificate (this will auto-configure the HTTPS virtual host)
sudo certbot --apache -d stage.yourdomain.com
```

After certbot runs, it will create an SSL-enabled virtual host that looks like:

```apache
<VirtualHost *:443>
    ServerName stage.yourdomain.com

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    RequestHeader set X-Forwarded-Proto "https"
    RequestHeader set X-Forwarded-For "%{REMOTE_ADDR}s"

    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/stage.yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/stage.yourdomain.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf

    ErrorLog ${APACHE_LOG_DIR}/wagtail_error.log
    CustomLog ${APACHE_LOG_DIR}/wagtail_access.log combined
</VirtualHost>
```

### 4. Update Environment Variables

Ensure your `.env` file has the correct settings:

```env
ALLOWED_HOSTS=stage.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://stage.yourdomain.com
```

**Important:** `CSRF_TRUSTED_ORIGINS` must include the `https://` prefix.

---

## Using PostgreSQL Database

PostgreSQL is **included by default** in docker-compose.yml. The database runs as a separate container and the web service automatically waits for it to be ready.

### Default Setup (Docker PostgreSQL)

The default configuration uses a PostgreSQL container. Just ensure your `.env` has matching passwords:

```env
DATABASE_URL=postgres://wagtail:your-secure-password@db:5432/wagtail
POSTGRES_PASSWORD=your-secure-password
```

### Option: Hetzner Managed Database

If you prefer using Hetzner's managed PostgreSQL:

1. Create a managed PostgreSQL database in Hetzner Cloud Console
2. Update your `.env` with the external connection string:

```env
DATABASE_URL=postgres://user:password@your-hetzner-db-host:5432/dbname
```

3. Comment out or remove the `db` service from `docker-compose.yml` if not needed

**Note:** SSL is automatically enabled for external database connections, but disabled for Docker internal connections (`db:5432`).

## Useful Commands

```bash
# View logs
docker compose logs -f

# Restart services
docker compose restart

# Stop services
docker compose down

# Update deployment
git pull
docker compose build
docker compose up -d

# Run Django management commands
docker compose exec web python manage.py shell
docker compose exec web python manage.py collectstatic
docker compose exec web python manage.py migrate

# Backup database (PostgreSQL)
docker compose exec db pg_dump -U wagtail wagtail > backup.sql

# Restore database
cat backup.sql | docker compose exec -T db psql -U wagtail wagtail
```

---

## Debugging the Container

### Inspect Container Filesystem

```bash
# Open a shell inside the running container
sudo docker compose exec web sh

# Check what's in the app directory
ls -la /app/

# Check if static files were collected
ls -la /app/staticfiles/

# Count static files
find /app/staticfiles -type f | wc -l

# Check if Tailwind CSS was built
ls -la /app/theme/static/css/dist/

# Check the Django settings being used
echo $DJANGO_SETTINGS_MODULE

# View settings values
python manage.py shell --settings=poxed.settings.build -c "from django.conf import settings; print('STATIC_ROOT:', settings.STATIC_ROOT)"
```

### Verify Static Files Discovery

```bash
# Check if Django can find specific static files
python manage.py findstatic wagtailadmin/css/core.css --settings=poxed.settings.build
python manage.py findstatic css/dist/styles.css --settings=poxed.settings.build

# List all static files Django can find
python manage.py shell --settings=poxed.settings.build -c "
from django.contrib.staticfiles import finders
count = 0
for finder in finders.get_finders():
    for path, storage in finder.list([]):
        count += 1
print(f'Total static files found: {count}')
"
```

---

## Troubleshooting

### Container won't start
```bash
docker compose logs web
docker compose logs db
```

### Static files not loading
```bash
# Static files are collected during Docker build
# If needed, rebuild the image:
docker compose build --no-cache
docker compose up -d
```

### Database connection errors
- Ensure `POSTGRES_PASSWORD` in `.env` matches the password in `DATABASE_URL`
- Check database container is running: `docker compose ps`
- Check database logs: `docker compose logs db`
- Verify the web container waited for db: `docker compose logs web | grep -i database`

### Build fails with static files error
The Docker build uses a special `build.py` settings file that avoids WhiteNoise manifest issues. If you still see errors:
```bash
# Force rebuild without cache
docker compose build --no-cache
```

### Static files show 0 copied / collectstatic not working

If `collectstatic` reports "0 static files copied" even though Django finds files, this is a known issue. You can manually copy static files inside the container:

```bash
# Enter the container
sudo docker compose exec web sh

# Create staticfiles directory if it doesn't exist
mkdir -p /app/staticfiles

# Copy static files from all sources
cp -r /usr/local/lib/python3.12/site-packages/wagtail/admin/static/* /app/staticfiles/
cp -r /usr/local/lib/python3.12/site-packages/wagtail/images/static/* /app/staticfiles/
cp -r /usr/local/lib/python3.12/site-packages/wagtail/snippets/static/* /app/staticfiles/
cp -r /usr/local/lib/python3.12/site-packages/wagtail/users/static/* /app/staticfiles/
cp -r /usr/local/lib/python3.12/site-packages/wagtail/embeds/static/* /app/staticfiles/
cp -r /usr/local/lib/python3.12/site-packages/wagtail/documents/static/* /app/staticfiles/ 2>/dev/null || true
cp -r /usr/local/lib/python3.12/site-packages/django/contrib/admin/static/* /app/staticfiles/
cp -r /app/poxed/static/* /app/staticfiles/
cp -r /app/theme/static/* /app/staticfiles/
cp -r /app/home/static/* /app/staticfiles/ 2>/dev/null || true

# Verify files were copied
find /app/staticfiles -type f | wc -l

# Exit container and restart
exit
sudo docker compose restart web
```

**Note:** This is a workaround. The static files will persist until the container is recreated. After a rebuild, you may need to repeat this process.

### 502 Bad Gateway
- Check if the web container is running: `docker compose ps`
- Check Gunicorn logs: `docker compose logs web`
- Verify port mapping in `docker-compose.yml`

### CSRF errors
- Ensure `CSRF_TRUSTED_ORIGINS` includes your domain with `https://`
- Check that `ALLOWED_HOSTS` is correctly set

## Security Checklist

- [ ] Change default `POSTGRES_PASSWORD` from 'changeme'
- [ ] Generate a secure `DJANGO_SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Configure `CSRF_TRUSTED_ORIGINS` with https:// URLs
- [ ] Use HTTPS (SSL certificate installed via Certbot)
- [ ] Configure firewall (ufw) - only expose ports 22, 80, 443
- [ ] Regular backups configured
- [ ] Monitor disk space
- [ ] Keep Docker and system updated

## Architecture Overview

The deployment uses a multi-container setup:

```
┌─────────────────────────────────────────────────────────────┐
│                    Hetzner Server                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                    Nginx                             │   │
│  │            (Reverse Proxy + SSL)                     │   │
│  │                 :80 / :443                           │   │
│  └─────────────────────┬───────────────────────────────┘   │
│                        │                                    │
│  ┌─────────────────────▼───────────────────────────────┐   │
│  │              Docker Compose                          │   │
│  │  ┌─────────────────┐    ┌─────────────────────────┐ │   │
│  │  │   web (Gunicorn)│◄──►│   db (PostgreSQL)       │ │   │
│  │  │   127.0.0.1:8000│    │   internal:5432         │ │   │
│  │  └─────────────────┘    └─────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Media Storage: Cloudinary (external)                       │
└─────────────────────────────────────────────────────────────┘
```

### Settings Files

| File | Purpose |
|------|---------|
| `poxed/settings/base.py` | Shared settings for all environments |
| `poxed/settings/dev.py` | Local development (SQLite, debug tools) |
| `poxed/settings/production.py` | Production (PostgreSQL, Cloudinary, security) |
| `poxed/settings/build.py` | Docker build only (simple static storage) |

---

## Running Alongside an Existing WordPress Site

If your Hetzner server already hosts a WordPress site, follow these additional steps:

### 1. Port Configuration

**Important:** Do NOT expose port 80 or 443 directly from Docker. Instead, use Nginx as a reverse proxy for both sites.

Update `docker-compose.yml` to only expose on localhost:

```yaml
services:
  web:
    ports:
      - "127.0.0.1:8000:8000"  # Only accessible locally, not from internet
```

### 2. Nginx Multi-Site Configuration

Create a new Nginx server block for the Wagtail site. Your existing WordPress config likely uses the default server or a specific domain.

Create `/etc/nginx/sites-available/wagtail-site`:

```nginx
upstream wagtail_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name wagtail.yourdomain.com;  # Use your actual domain

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name wagtail.yourdomain.com;

    # SSL certificates (use certbot to generate)
    ssl_certificate /etc/letsencrypt/live/wagtail.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/wagtail.yourdomain.com/privkey.pem;

    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;

    # Logging (separate from WordPress)
    access_log /var/log/nginx/wagtail_access.log;
    error_log /var/log/nginx/wagtail_error.log;

    # Max upload size
    client_max_body_size 100M;

    location / {
        proxy_pass http://wagtail_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static files - served by Nginx for better performance
    # Uncomment if you want Nginx to serve static files directly
    # location /static/ {
    #     alias /path/to/aprils-site/staticfiles/;
    #     expires 30d;
    #     add_header Cache-Control "public, immutable";
    # }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/wagtail-site /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 3. SSL Certificate for New Domain

Get a certificate for the Wagtail domain:
```bash
sudo certbot --nginx -d wagtail.yourdomain.com
```

Or if using the same domain with a subdirectory (not recommended):
```bash
# Add the domain to your existing certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com -d wagtail.yourdomain.com
```

### 4. Resource Considerations

Running both sites on the same server means sharing resources:

| Resource | Recommendation |
|----------|---------------|
| **RAM** | Minimum 4GB total (WordPress ~1GB, Wagtail ~512MB-1GB, Nginx/MySQL/PostgreSQL) |
| **CPU** | 2+ vCPUs recommended |
| **Disk** | Monitor usage, especially media uploads |

Update `docker-compose.prod.yml` to limit Wagtail's resource usage:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### 5. Database Isolation

**Option A: Separate databases (Recommended)**
- WordPress: MySQL/MariaDB (existing)
- Wagtail: PostgreSQL in Docker or Hetzner managed database

**Option B: Shared PostgreSQL** (if WordPress isn't using MySQL)
- Create separate database and user for each application

```bash
# If using PostgreSQL for both (connect to PostgreSQL)
sudo -u postgres psql

CREATE DATABASE wagtail_db;
CREATE USER wagtail_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE wagtail_db TO wagtail_user;
\q
```

### 6. Firewall Configuration

Ensure your firewall only exposes necessary ports:

```bash
sudo ufw status

# Should show:
# 22/tcp (SSH)
# 80/tcp (HTTP)
# 443/tcp (HTTPS)

# Do NOT open port 8000 - it should only be accessible via localhost
```

### 7. Backup Strategy

Set up separate backups for each site:

```bash
# WordPress backup (example with existing setup)
# ... your existing WordPress backup ...

# Wagtail backup script - /opt/scripts/backup-wagtail.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups/wagtail

# Database backup (if using Docker PostgreSQL)
docker compose -f /path/to/aprils-site/docker-compose.yml exec -T db \
    pg_dump -U wagtail wagtail > $BACKUP_DIR/db_$DATE.sql

# Or if using external database
# pg_dump -h hostname -U wagtail wagtail > $BACKUP_DIR/db_$DATE.sql

# Keep last 7 days
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
```

### 8. Monitoring

Monitor both applications separately:

```bash
# Check Wagtail container status
docker compose -f /path/to/aprils-site/docker-compose.yml ps
docker compose -f /path/to/aprils-site/docker-compose.yml logs --tail=50

# Check resource usage
docker stats

# Check Nginx status
sudo systemctl status nginx
sudo tail -f /var/log/nginx/wagtail_error.log
```

### 9. Update Strategy

Update each site independently:

```bash
# Update WordPress (use your existing process)
# ...

# Update Wagtail
cd /path/to/aprils-site
git pull
docker compose build
docker compose up -d
```

### 10. Common Issues

| Issue | Solution |
|-------|----------|
| **502 Bad Gateway** | Check if Docker container is running: `docker compose ps` |
| **Nginx won't start** | Check config: `nginx -t`, check logs: `journalctl -u nginx` |
| **Both sites show same content** | Check `server_name` in Nginx configs |
| **SSL certificate issues** | Run `certbot renew --dry-run` to test |
| **Database connection refused** | Check if database container is running, verify `DATABASE_URL` |
| **Out of memory** | Add swap or reduce container limits |

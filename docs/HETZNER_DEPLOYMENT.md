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
DJANGO_SECRET_KEY=your-generated-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (use PostgreSQL for production)
DATABASE_URL=postgres://user:password@host:5432/dbname

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Email
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-password
```

### 4. Build and Deploy

```bash
# Build the Docker image
docker compose build

# Start the containers
docker compose up -d

# Check logs
docker compose logs -f web

# Run migrations (if not done automatically)
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser
```

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

## Using PostgreSQL Database

### Option 1: Hetzner Managed Database

1. Create a managed PostgreSQL database in Hetzner Cloud Console
2. Copy the connection string to your `.env` file

### Option 2: Self-hosted PostgreSQL with Docker

Uncomment the PostgreSQL service in `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:16-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=wagtail
      - POSTGRES_USER=wagtail
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    restart: unless-stopped

volumes:
  postgres_data:
```

Update `.env`:
```env
DATABASE_URL=postgres://wagtail:yourpassword@db:5432/wagtail
POSTGRES_PASSWORD=yourpassword
```

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

## Troubleshooting

### Container won't start
```bash
docker compose logs web
```

### Static files not loading
```bash
docker compose exec web python manage.py collectstatic --noinput
```

### Database connection errors
- Check `DATABASE_URL` in `.env`
- Ensure database container is running: `docker compose ps`
- Check database logs: `docker compose logs db`

### 502 Bad Gateway
- Check if the web container is running: `docker compose ps`
- Check Gunicorn logs: `docker compose logs web`
- Verify port mapping in `docker-compose.yml`

### CSRF errors
- Ensure `CSRF_TRUSTED_ORIGINS` includes your domain with `https://`
- Check that `ALLOWED_HOSTS` is correctly set

## Security Checklist

- [ ] Change default passwords
- [ ] Set `DEBUG=False`
- [ ] Use HTTPS (SSL certificate installed)
- [ ] Configure firewall (ufw)
- [ ] Regular backups configured
- [ ] Monitor disk space
- [ ] Keep Docker and system updated

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

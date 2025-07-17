# 🚀 Deployment Guide: White-Labeled Wagtail Blog

## Table of Contents
1. Project Overview
2. Quickstart
3. Prerequisites
4. Installation
5. Configuration
6. Django Tailwind Setup
7. Deployment
8. Updating & Upgrading
9. Production Checklist
10. Troubleshooting & FAQ
11. Further Reading

---

## 1. Project Overview
This project is a modular, white-labeled Wagtail blog and portfolio application. It features:
- Modular apps: blog, portfolio, CV, timeline, home, base, search, theme
- Highly customizable StreamField blocks for flexible content
- Tailwind CSS integration for modern styling
- Cloudinary support for media storage (optional)
- Docker and Heroku deployment support
- Custom navigation, header/footer, and social links
- Admin UI for content, users, and settings
- Email/contact form support

---

## 2. Quickstart
Experienced users can deploy locally with:
```bash
git clone <your-repo-url>
cd <project-folder>
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
cp .env.example .env  # Or create .env as below
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py tailwind install
uv run python manage.py tailwind build
uv run python manage.py collectstatic
uv run python manage.py runserver
```

---

## 3. Prerequisites
- Python 3.10+
- Git
- Node.js & npm (for TailwindCSS/static assets)
- Docker (optional, for containerized deployment)
- Cloudinary account (for media storage, if used)
- Email service credentials (for contact form)
- Server or cloud platform (Heroku, DigitalOcean, AWS, etc.)
- [uv](https://github.com/astral-sh/uv) (for Python dependency management)
- [openssl](https://www.openssl.org/) (for generating a Django secret key)

---

## 4. Installation

### 4.1. Clone the Repository
```bash
git clone <your-repo-url>
cd <project-folder>
```

### 4.2. Set Up a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 4.3. Install Python Dependencies with uv
If you don't have `uv` installed, follow the instructions at https://github.com/astral-sh/uv#installation

```bash
uv pip install -r requirements.txt
```

---

## 5. Configuration

### 5.1. Create the .env File
Create a blank `.env` file and add the required environment variables (the secret key will be added in the next step):

```bash
touch .env
echo "DJANGO_SECRET_KEY=" >> .env
echo "DJANGO_DEBUG=False" >> .env
echo "DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com" >> .env
echo "DATABASE_URL=sqlite:///db.sqlite3" >> .env
echo "CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>" >> .env
echo "EMAIL_HOST=smtp.yourprovider.com" >> .env
echo "EMAIL_HOST_USER=your@email.com" >> .env
echo "EMAIL_HOST_PASSWORD=yourpassword" >> .env
echo "EMAIL_PORT=587" >> .env
echo "EMAIL_USE_TLS=True" >> .env
```

#### Environment Variable Security
- Never commit your `.env` file to version control.
- Use a secrets manager or environment variables in production.
- Rotate secrets regularly.

### 5.2. Generate and Add a Django Secret Key
Generate a secure Django secret key and add it to your `.env` file:

```bash
SECRET_KEY=$(openssl rand -base64 48 | tr -d '\n' | head -c 50)
sed -i "s|DJANGO_SECRET_KEY=|DJANGO_SECRET_KEY=$SECRET_KEY|" .env
```

On macOS, use `sed -i ''` instead of `sed -i`:

```bash
SECRET_KEY=$(openssl rand -base64 48 | tr -d '\n' | head -c 50)
sed -i '' "s|DJANGO_SECRET_KEY=|DJANGO_SECRET_KEY=$SECRET_KEY|" .env
```

### 5.3. Database & Media Configuration
- **Local:** Default is SQLite and local media in `media/`.
- **Production:** Use Postgres (recommended) and a cloud media backend (e.g., Cloudinary).
- See `poxed/settings/base.py` for database and storage settings.
- For Cloudinary, set `CLOUDINARY_URL` in `.env`.
- For other storage, see [Django storages](https://django-storages.readthedocs.io/).

---

## 6. Django Tailwind Setup

### 6.1. Install Tailwind CSS Dependencies
```bash
uv run python manage.py tailwind install
```
### 6.2. Development: Start Tailwind Watcher
To enable live Tailwind CSS compilation and browser reload during development:
```bash
uv run python manage.py tailwind start
```
(Leave this running in a separate terminal while developing.)

### 6.3. Production: Build Tailwind CSS
Before deploying, build the production-optimized CSS:
```bash
uv run python manage.py tailwind build
```

---

## 7. Deployment

### 7.1. Database Migrations
```bash
uv run python manage.py migrate
```

### 7.2. Create a Superuser
```bash
uv run python manage.py createsuperuser
```

### 7.3. Collect Static Files
```bash
uv run python manage.py collectstatic
```

### 7.4. Docker (Recommended)
```bash
docker build -t wagtail-blog .
docker run -d -p 8000:8000 --env-file .env wagtail-blog
```

### 7.5. Heroku
- Add Heroku remote:  
  `heroku git:remote -a your-app-name`
- Set config vars in Heroku dashboard or via CLI.
- Deploy:  
  `git push heroku main`

### 7.6. Manual (Linux Server)
- Set up a production web server (e.g., Gunicorn + Nginx)
- Set environment variables
- Run migrations, collectstatic, and start the server using `uv run python manage.py ...`

#### Zero Downtime Deployment
- Use a process manager (e.g., systemd, supervisor, or Heroku dynos) to restart the app gracefully.
- Run migrations before switching traffic to new code.
- For Docker, use rolling updates or blue/green deployment if possible.

---

## 8. Updating & Upgrading
- Pull the latest code: `git pull origin main` (or your branch)
- Reinstall dependencies if `requirements.txt` changed: `uv pip install -r requirements.txt`
- Run migrations: `uv run python manage.py migrate`
- Rebuild static assets: `uv run python manage.py tailwind build && uv run python manage.py collectstatic`
- Restart your server/process manager/Docker container

---

## 9. Production Checklist
- [ ] Set `DJANGO_DEBUG=False` in `.env`
- [ ] Set `DJANGO_ALLOWED_HOSTS` to your domain(s)
- [ ] Use a secure, unique `DJANGO_SECRET_KEY`
- [ ] Use Postgres or another production-grade database
- [ ] Use a cloud media backend (e.g., Cloudinary)
- [ ] Set up HTTPS (SSL/TLS)
- [ ] Set up regular database and media backups
- [ ] Set up monitoring and error reporting
- [ ] Restrict admin access to trusted users
- [ ] Rotate secrets regularly
- [ ] Review and update dependencies

---

## 10. Troubleshooting & FAQ
- **Static files not loading:** Ensure `collectstatic` has been run and static files are served by your web server.
- **Emails not sending:** Check email configuration in `.env` and server logs.
- **Media not uploading:** Verify Cloudinary or local media configuration.
- **Page not found (404):** Check page tree in Wagtail admin and ensure the page is published.
- **Database errors:** Check your `DATABASE_URL` and database server status.
- **Docker issues:** Check container logs with `docker logs <container-id>`.
- **Heroku issues:** Use `heroku logs --tail` and check config vars.
- **How do I update the app?** See section 8 above.

---

## 11. Further Reading
- [Wagtail documentation](https://docs.wagtail.org/)
- [Django documentation](https://docs.djangoproject.com/)
- [Django Tailwind](https://django-tailwind.readthedocs.io/)
- [Cloudinary for Django](https://cloudinary.com/documentation/django_integration)
- [Docker documentation](https://docs.docker.com/)
- [Heroku Django deployment](https://devcenter.heroku.com/articles/deploying-python)
- See `poxed/settings/base.py`, `Dockerfile`, and `theme/static_src/` for configuration examples. 
# =============================================================================
# Multi-stage Dockerfile for Wagtail/Django with Tailwind CSS
# Optimized for Hetzner deployment
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Build stage - Install dependencies and build assets
# -----------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS builder

# Install system packages required for building
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for Tailwind CSS build
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Build Tailwind CSS (needs npm dependencies first)
RUN cd theme/static_src && npm install && npm run build

# -----------------------------------------------------------------------------
# Stage 2: Production stage - Minimal runtime image
# -----------------------------------------------------------------------------
FROM python:3.12-slim-bookworm AS production

# Add user that will be used in the container
RUN useradd --create-home wagtail

# Port used by this container to serve HTTP
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=poxed.settings.production

# Install runtime system packages only
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq5 \
    libmariadb3 \
    libjpeg62-turbo \
    zlib1g \
    libwebp7 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=wagtail:wagtail . .

# Copy built Tailwind CSS from builder stage
COPY --from=builder --chown=wagtail:wagtail /app/theme/static/css/dist /app/theme/static/css/dist

# Set ownership for the app directory
RUN chown -R wagtail:wagtail /app

# Switch to non-root user
USER wagtail

# Collect static files (requires some env vars to be set, using dummy values for build)
RUN DJANGO_SECRET_KEY=build-secret-key \
    CLOUDINARY_CLOUD_NAME=dummy \
    CLOUDINARY_API_KEY=dummy \
    CLOUDINARY_API_SECRET=dummy \
    python manage.py collectstatic --noinput --clear

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/admin/login/')" || exit 1

# Runtime command
# Note: Migrations should ideally be run separately, but included here for convenience
CMD set -xe; \
    python manage.py migrate --noinput; \
    gunicorn poxed.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 2 \
        --threads 4 \
        --worker-class gthread \
        --worker-tmp-dir /dev/shm \
        --access-logfile - \
        --error-logfile - \
        --capture-output \
        --enable-stdio-inheritance

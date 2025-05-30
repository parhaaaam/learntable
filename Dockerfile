# --- Build Stage: Install Python Dependencies ---
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DEFAULT_TIMEOUT=100
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies including MySQL dev packages
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    python3-dev \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Configure pip to use a more reliable mirror
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt || \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- Final Stage ---
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=learntable.settings

WORKDIR /app

# Install system dependencies including MySQL client
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python wheels from builder stage
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/staticfiles

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Django development server
# Note: For production, you should use gunicorn or uvicorn
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 
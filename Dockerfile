# Dockerfile - Simple version without uv
FROM python:3.11-slim

WORKDIR /app

# Set Python to run in lightweight mode
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/db

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
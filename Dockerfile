# Use Python 3.12 slim for smaller image and PyTorch CPU compatibility
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for OpenCV headless and other packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install first for caching
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install packages without cache to reduce image size
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of your application code
COPY . /app

# Expose the default port (Railway uses $PORT automatically)
EXPOSE 8000

# Start Flask app using Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-8000}", "run_app:app"]

# Use a lightweight but stable Python base
FROM python:3.9-slim-buster

# Metadata
LABEL maintainer="yourname@example.com"
LABEL description="Customized YOLOv5/v8 Fire Detection Environment"

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system-level dependencies required for OpenCV, Git, and graphics acceleration
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /usr/src/app

# Upgrade pip and install common heavy ML dependencies first (improves Docker caching)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements file and install specific python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code, model weights, and scripts
COPY . .

# Create a non-root user for security compliance (Optional but recommended)
RUN useradd -m appuser && chown -R appuser /usr/src/app
USER appuser

# Expose a port if your fire detection has a web UI (Flask/FastAPI/Streamlit)
# EXPOSE 8000

# Script to run when container starts
CMD ["python", "detect.py"]

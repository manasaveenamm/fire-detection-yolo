# Changed from buster to bookworm to fix the 404 apt-get update error
FROM python:3.9-slim-bookworm

# Metadata
LABEL description="Customized YOLOv5/v8 Fire Detection Environment"

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system-level dependencies required for OpenCV and graphics acceleration
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

# Upgrade pip and install common heavy ML dependencies first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements file and install specific python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your source code, model weights, and scripts
COPY . .

# Script to run when container starts
CMD ["python", "detect.py"]

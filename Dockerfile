FROM python:3.9-slim

# Install only the absolute bare minimum system library needed for OpenCV Headless
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip to the latest stable release
RUN pip install --no-cache-dir --upgrade pip

# Copy and install dependencies safely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model weights
COPY . .

# Run the live detector application
CMD ["python", "detect.py"]

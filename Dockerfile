FROM python:3.9-slim

# Install the critical rendering libraries needed for OpenCV on headless Linux systems
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libgl1 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip to the latest stable release
RUN pip install --no-cache-dir --upgrade pip

# Copy and install dependencies safely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Force install the headless version of OpenCV to bypass any GUI library dependencies
RUN pip install --no-cache-dir opencv-python-headless

# Copy the application code and model weights
COPY . .

# Run the live detector application
CMD ["python", "detect.py"]

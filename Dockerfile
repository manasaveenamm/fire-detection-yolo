# Use a pre-compiled image that already has PyTorch installed to save space
FROM ultralytics/ultralytics:latest-cpu

WORKDIR /app

# Copy requirements and remove torch/torchvision from them to prevent re-downloading
COPY requirements.txt .
RUN sed -i '/torch/d' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Force install the headless version of OpenCV to save space and avoid GUI issues
RUN pip install --no-cache-dir opencv-python-headless

# Copy the rest of the application
COPY . .

CMD ["python", "detect.py"]

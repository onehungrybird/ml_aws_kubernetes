# Use a lightweight Python image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and model
COPY src/ ./src
COPY models/ ./models
COPY app.py .

# Expose the API port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

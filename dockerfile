# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code to the container
COPY src/ /app/src
COPY data/  /app/data
COPY questions.txt /app/
# Default command to run the application with --default
CMD ["python", "src/main.py", "--default"]
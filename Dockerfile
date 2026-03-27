# Image
FROM python:3.11-slim

# Project Direction
WORKDIR /gwt

# Copy Requirements
COPY /requirements.txt .

# Install Packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project
COPY app/ ./app

# Port
EXPOSE 8000

# Run Server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
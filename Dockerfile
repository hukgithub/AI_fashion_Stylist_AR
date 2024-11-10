# Use a base image with Python and necessary dependencies
FROM python:3.8-slim

# Set working directories
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# Install dependencies for FastAPI
WORKDIR /app/api
COPY ./api/requirements.txt /app/api/requirements.txt
RUN pip install -r requirements.txt

# Copy application files
COPY . /app

# Expose ports for Streamlit (8501) and FastAPI (8000)
EXPOSE 8501
EXPOSE 8000

# Run FastAPI and Streamlit concurrently
CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.enableCORS=false"]

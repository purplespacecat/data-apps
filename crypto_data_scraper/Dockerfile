# Use official Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app/crypto_data_scraper

# Copy only the requirements first to leverage Docker cache for faster builds
COPY crypto_data_scraper/requirements.txt .

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment and install dependencies
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Update PATH to use venv by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the application
COPY crypto_data_scraper/ .

# Run tests using virtual environment
RUN pytest tests

# If tests pass, run the Streamlit app
CMD ["streamlit", "run", "app.py"]

# Use official Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements first to leverage Docker cache for faster builds
COPY requirements.txt .

# Create a virtual environment
RUN python -m venv /opt/venv

# Activate virtual environment and install dependencies
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Update PATH to use venv by default
ENV PATH="/opt/venv/bin:$PATH"

# Set Python path
ENV PYTHONPATH=/app

# Copy application files
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]
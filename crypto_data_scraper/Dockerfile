# Dockerfile

FROM python:3.10-slim

# Set working directory
WORKDIR /app/crypto_data_scraper

# Copy requirements and install dependencies
COPY crypto_data_scraper/requirements.txt .
RUN python -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Set PATH to use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy the rest of the application code
COPY crypto_data_scraper/ .

# Declare the build argument
ARG RUN_TESTS=true

# Conditionally run tests if RUN_TESTS is true
RUN if [ "$RUN_TESTS" = "true" ]; then pytest tests; else echo "Skipping tests"; fi

# Default command (optional)
CMD ["streamlit", "run", "app.py"]

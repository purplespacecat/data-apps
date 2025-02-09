# Use official Python image as the base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements first to leverage Docker cache for faster builds
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run tests before building the final image
RUN pip install pytest && pytest tests

# If tests pass, proceed to run the Streamlit app
CMD ["streamlit", "run", "app.py"]

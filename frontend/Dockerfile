# Dockerfile-frontend

# Image base
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy dependency files and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of the project files
COPY . /app

# Command to run the application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
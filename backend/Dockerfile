# Dockerfile-backend

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
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
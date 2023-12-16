# Use the official Python 3.12 image as the base image
FROM python:3.12

# Set the working directory in the container to /server
WORKDIR /server

# Copy the requirements file into the container
COPY requirements.txt ./

# Create a virtual environment in the container
RUN python -m venv .venv

# Activate the virtual environment
ENV PATH="/server/.venv/bin:$PATH"

# Install dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy the src directory into the container
COPY src/ ./src/

# Set the working directory to /server/src
WORKDIR /server/src

# Command to run the application
CMD ["python", "./app.py"]

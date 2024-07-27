# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

# Install Octokit
RUN npm install @octokit/core

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose port 11434 to the outside world
EXPOSE 11434

# Start Ollama service and pull the Llama3 model
RUN nohup ollama serve & \
    sleep 10 && \
    ollama pull llama3

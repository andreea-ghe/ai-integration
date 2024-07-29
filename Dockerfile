# Use an official Python runtime as a parent image
FROM python:3.11-slim AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg \
    git \
    jq && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Octokit and node-fetch using npm
RUN npm install @octokit/core node-fetch

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install ollama litellm python-dotenv openai

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the script to pull the model
COPY pull_model.sh /app/pull_model.sh

# Make the script executable
RUN chmod +x /app/pull_model.sh

# Pull the Llama3 model
RUN /app/pull_model.sh

# Use a smaller runtime image
FROM python:3.11-slim

# Copy the dependencies and model from the builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /root/.ollama /root/.ollama
COPY --from=builder /app /app

# Expose port 11434 to the outside world
EXPOSE 11434

# Start Ollama service and keep the container running
CMD nohup ollama serve > ollama.log 2>&1 & tail -f /dev/null

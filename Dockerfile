# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Install Ollama (without sudo)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Start the Ollama service and pull the llama3 model
RUN nohup ollama serve & \
    sleep 5 && \
    ollama run llama3

# Specify the command to run your application (modify this as per your needs)
CMD ["python", "your_script.py"]

# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Download the model (example: llama3) after installing the dependencies
RUN python -c "import ollama; ollama.download_model('llama3')"

# Specify the command to run your application (this will be modified as per your needs)
CMD ["python", "your_script.py"]

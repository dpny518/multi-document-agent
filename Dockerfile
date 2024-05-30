# Use the official Python image from the Docker Hub
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install bash and wget
RUN apt-get update && apt-get install -y bash wget

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for the papers
RUN mkdir -p /app/papers

# Copy the shell script to the container
COPY download_papers.sh /app/

# Make the shell script executable
RUN chmod +x /app/download_papers.sh

# Use bash to run the shell script
RUN /bin/bash /app/download_papers.sh

# Copy the rest of the application code to /app
COPY . /app

# Copy the .env file to the container
COPY .env /app/

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

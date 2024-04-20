FROM ubuntu:22.04

# Update package lists and install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip

WORKDIR /app

# Copy the current directory into the container
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port 4000
EXPOSE 4000

# Command to run the application
CMD ["python3", "-u", "main.py"]

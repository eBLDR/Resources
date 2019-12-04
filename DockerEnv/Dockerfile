# Use an image - The image will be searched locally first, and the in
# DockerHub repository
FROM python:3.6-slim

# Set the container working directory to <path>
WORKDIR /app

# Copy <src> from machine into the container <path>
COPY . /app
# ADD is an equivalent to COPY, but allows the source to be an URL

# Run a command inside the container
RUN pwd

# Make port available to the world outside this container
EXPOSE 80

# Many ports can be exposed
# EXPOSE 5000 5002 5004

# Define environment variable
ENV NAME mydockerenv

# Run this when the container launches - [application, filename]
CMD ["python", "app.py"]

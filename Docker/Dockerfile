# Use an image - The image will be searched locally first, and the in
# DockerHub repository:
FROM <image>[:<tag>] [AS <name>]
# FROM scratch - to use an image which is empty.

# Sets the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD
# instructions that follow it in the Dockerfile. If the <path> doesn't exist,
# it will be created:
WORKDIR <path>

# Copies new files or directories from <src> and adds them to the filesystem
# of the container at the path <dest>:
COPY <src> <dest>
# ADD is an equivalent to COPY, but allows the source to be an URL

# Run a command inside the container when the image is built:
RUN <command>

# `exec` form:
RUN ["executable", "param1", "param2"]

# Informs that the container listens on the specified network ports at runtime:
EXPOSE <port>

# Many ports can be exposed:
# EXPOSE 5000 5002 5004

# Define environment variables:
ENV <key> <value>

# Creates a mount point with the specified name and marks it as holding
# externally mounted volumes from native host or other containers:
VOLUME ["/data"]

# Run this when the container launches (not when building):
CMD ["executable","param1","param2"]
# There can only be one CMD instruction in a Dockerfile. If more are found,
# then only the last CMD will take effect.
# The container stops when this process dies.

# Allows to configure a container that will run as an executable:
ENTRYPOINT ["executable", "param1", "param2"]

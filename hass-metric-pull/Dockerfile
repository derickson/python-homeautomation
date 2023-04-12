# Use an official Python runtime as a parent image
FROM python:3.8.10-slim-buster

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get upgrade -y python-virtualenv

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY *.py /app/
COPY *.txt /app/
COPY *.sh /app/

# Create a Python virtual environment
RUN python -m venv env

# Activate the virtual environment and install required packages
RUN . env/bin/activate && \
    pip install --trusted-host pypi.python.org -r requirements.txt 


# RUN pip install requests
# Make port 80 available to the world outside this container
#EXPOSE 80

# Run app.py when the container launches
CMD ["/bin/bash", "run.sh"]

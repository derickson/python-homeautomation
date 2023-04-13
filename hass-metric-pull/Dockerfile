# Use an official Python runtime as a parent image
FROM python:3.8.10-slim-buster

RUN apt-get update && \
    apt-get install -y curl 
    
RUN python3 -m pip install --upgrade pi  

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY *.py /app/
COPY *.txt /app/
COPY *.sh /app/

# RUN pip install requests
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt 



# Run app.py when the container launches
CMD ["/bin/bash", "run.sh"]
# CMD ["tail", "-f", "/dev/null"]

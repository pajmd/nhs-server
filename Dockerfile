# Dockerfile
# image intened to be save in my own registry
# docker run -d -p 5001:5000 --restart=always --name registry registry:2
# docker build --tag=pjmd-ubuntu:5001/nhs-server-app:0.1 .

# Use an official Python runtime as a parent image
# FROM python:3.6-slim
FROM nhs-ui

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
# COPY ../../../../js_workspace/VueProjects/nhs-ui/dist /app/nhs-ui

RUN echo $(ls -1R .)

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
# The EXPOSE instruction does not actually publish the port. It functions as a type of documentation between the person who
# builds the image and the person who runs the container, about which ports are intended to be published
EXPOSE 5000

# Define environment variable (not used)
ENV NAME World

# need to extend PYHTONPATH so CMD works
ENV PYTHONPATH="$PYTHONPATH:/app"

# NHS-UI built distribution (files copied over in image nhs-ui)
ENV NHS_UI_DIST="nhs-ui"

# Run app.py when the container launches
CMD ["python", "app/run.py"]

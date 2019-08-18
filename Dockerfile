# Dockerfile
# image intened to be save in my own registry
# docker run -d -p 5001:5000 --restart=always --name registry registry:2
# docker build --tag=pjmd-ubuntu:5001/nhs-server-app:0.1 .
#
# with git versioning: 
# --------------------
#
# DON'T FORGET TO FETCH to get the latest tags/versions (at least from PYCHARM)
#
# (inpired from https://blog.scottlowe.org/2017/11/08/how-tag-docker-images-git-commit-information/ and https://blog.container-solutions.com/tagging-docker-images-the-right-way)
#
# docker build -t nhs-server-app --build-arg GIT_VERSION=$(git describe) .
#
# To find out the image version: docker inspect <image name> | grep labels 
#
#
# git commands:
# to push a tag: git push --follow-tags
# to pull tags (created in git hub): git fetch
# to list tags: git tag [-l]
# to get the latest version: git describe
#


# Use an official Python runtime as a parent image
# FROM python:3.6-slim
FROM pjmd-ubuntu:5001/nhs-ui:v0.0.1

# labeling this build with the version of the web app passed as argument in the docker build command
#
# See Makfile
#
# it is recommended to use the reverse dns notaion for a label: com.pjmd.git_version
#

ARG GIT_VERSION=unspecified
LABEL git_version=$GIT_VERSION

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
# flask port
# EXPOSE 5000 
# WSGI port (cherrypy)
EXPOSE 8000

# Define environment variable (not used)
ENV NAME World

# need to extend PYHTONPATH so CMD works
ENV PYTHONPATH="$PYTHONPATH:/app"

# NHS-UI built distribution (files copied over in image nhs-ui)
ENV NHS_UI_DIST="nhs-ui"

# Run flask run.py when the container launches
# CMD ["python", "app/run.py"]

# Run CherryPy wsgi run.py when the container launches
CMD ["python", "app/wsgi_server.py"]

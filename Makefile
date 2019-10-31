# 
# This Makefile build the nhs-server-app image, tags it and pushes to local docker repos
#
NAME   := pjmd-ubuntu.com/nhs-server-app
TAG    := $$(git describe --tag)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest
 
build:
	@docker build -t ${IMG} --build-arg GIT_VERSION=${TAG} .
	@docker tag ${IMG} ${LATEST}
 
push:
	@docker push ${IMG}
 
# login:
#   @docker log -u ${DOCKER_USER} -p ${DOCKER_PASS}

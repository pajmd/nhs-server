# 
# This Makefile build the nhs-server-app image, tags it and pushes to local docker repos
#
APP    := nhs-server-app
PUBLIC_REPO := pajmd
NAME   := pjmd-ubuntu.com/${APP}
TAG    := $$(git describe --tag)
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest
PUBLIC_IMG := ${PUBLIC_REPO}/${APP}:${TAG}

all: push

build:
	@git fetch origin
	@docker build -t ${IMG} --build-arg GIT_VERSION=${TAG} .
	@docker tag ${IMG} ${LATEST}
	@docker tag ${IMG} ${PUBLIC_IMG}

push: build
	@docker push ${IMG}
 
# login:
#   @docker log -u ${DOCKER_USER} -p ${DOCKER_PASS}

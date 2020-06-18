NAME = nexus.itass.local:14010/roles-api-pgsql
BUILD_VERSION = $(bamboo_planRepository_branch).$(bamboo_buildNumber)

.PHONY: all build tag_latest push

all: build


help:
	@echo "lint - check style with flake8"
	@echo "build - Build a docker image with current version"
	@echo "tag_latest - Tag current docker image tag with tag latest"
	@echo "push - tag with latest and push to docker repository"

lint:
	flake8

build:
	docker build -t $(NAME):$(BUILD_VERSION) --rm .

tag_latest:
	docker tag $(NAME):$(BUILD_VERSION) $(NAME):latest

push: tag_latest
	@if ! docker images $(NAME) | awk '{ print $$2 }' | grep -q -F $(BUILD_VERSION); then echo "$(NAME) version $(BUILD_VERSION) is not yet built. Please run 'make build'"; false; fi
	docker push $(NAME):$(BUILD_VERSION)
	docker push $(NAME):latest
	@echo "*** Don't forget to create a tag by creating an release."

stub:
	echo $(BUILD_VERSION) > version

echo_version:
	@echo "$(BUILD_VERSION)"

## Makefile for bgpstream docker container

build: Dockerfile 
	docker build -t salt_stack .

shell: build
	docker run --hostname salt_stack \
		-v $$(pwd)/work:/work \
		-ti salt_stack /bin/bash

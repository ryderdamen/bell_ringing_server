IMAGE_NAME=gcr.io/radical-sloth/youtube-follower-count
IMAGE_TAG=0.0.1
GCR_NAME=youtube-subscriber-count

.PHONY: build
build:
	@docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

.PHONY: run
run:
	@docker run \
		-v $(shell pwd )/src:/code \
		-p 5000:5000 $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: install
install:
	@make build

.PHONY: push
push:
	@docker push $(IMAGE_NAME):$(IMAGE_TAG)

.PHONY: deploy
deploy:
	@make build
	@make push
	@gcloud run deploy $(GCR_NAME) \
		--image $(IMAGE_NAME):$(IMAGE_TAG) \
		--region us-central1 \
		--port 5000 \
		--concurrency 80 \
		--cpu 1 \
		--max-instances 1 \
		--timeout 5 \
		--memory 128Mi \
		--platform managed \
		--allow-unauthenticated \
		--project radical-sloth

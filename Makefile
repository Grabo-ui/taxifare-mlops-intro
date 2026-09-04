include .env
export

run-api:
	uv run uvicorn api.fast:app --reload

build-docker-local:
	docker build --tag=$(DOCKER_IMAGE_NAME):dev .

docker-run:
	docker run -e PORT=8000 -p 8000:8000 --env-file .env $(DOCKER_IMAGE_NAME):dev

build-docker-prod:
	docker build --platform linux/amd64 -t $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/$(ARTIFACTSREPO)/$(DOCKER_IMAGE_NAME):prod .

push-docker:
	docker push $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/$(ARTIFACTSREPO)/$(DOCKER_IMAGE_NAME):prod

deploy:
	gcloud run deploy --image $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/$(ARTIFACTSREPO)/$(DOCKER_IMAGE_NAME):prod --memory 2Gi --region $(GCP_REGION) --env-vars-file .env.yaml

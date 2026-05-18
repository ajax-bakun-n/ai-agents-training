.PHONY: apply clean build push

apply:
	kubectl apply -f k8s/

clean:
	kubectl delete -f k8s/ --ignore-not-found

build:
	docker build -t ghcr.io/ajax-bakun-n/lab4-a2a-agent:latest ./agent

push:
	docker push ghcr.io/ajax-bakun-n/lab4-a2a-agent:latest
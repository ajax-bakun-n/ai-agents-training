.PHONY: apply apply-max gitops secret build push clean

apply:
	@test -f .env || (echo "copy .env.example to .env and fill in keys" && exit 1)
	kubectl apply -k .

apply-max:
	@test -f .env || (echo "copy .env.example to .env and fill in keys" && exit 1)
	kubectl apply -f kagent/model-config.yaml
	kubectl apply -f kagent/custom-mcp-server.yaml
	kubectl apply -f kagent/custom-agent.yaml

secret:
	@test -f .env || (echo "copy .env.example to .env and fill in keys" && exit 1)
	kubectl create secret generic anthropic-api-key \
	  --from-env-file=.env --namespace kagent --dry-run=client -o yaml | kubectl apply -f -

gitops: secret
	kubectl apply -f gitops/gitrepository.yaml
	kubectl apply -f gitops/kustomization.yaml

build:
	docker build -t ghcr.io/ajax-bakun-n/lab2-mcp-server:latest ./mcp-server

push:
	docker push ghcr.io/ajax-bakun-n/lab2-mcp-server:latest

clean:
	kubectl delete -k . --ignore-not-found

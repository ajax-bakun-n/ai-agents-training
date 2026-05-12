.PHONY: apply apply-max secret gitops build push clean

# Create API key secret manually before running apply.
# See README for instructions.

apply:
	kubectl apply -k .

apply-max:
	kubectl apply -f kagent/model-config.yaml
	kubectl apply -f kagent/custom-mcp-server.yaml
	kubectl apply -f kagent/custom-agent.yaml

secret:
	kubectl create secret generic anthropic-api-key \
	  --from-literal=ANTHROPIC_API_KEY=<your-anthropic-api-key> \
	  --from-literal=OPENAI_API_KEY=<your-openai-api-key> \
	  --namespace kagent --dry-run=client -o yaml | kubectl apply -f -

gitops:
	kubectl apply -f gitops/gitrepository.yaml
	kubectl apply -f gitops/kustomization.yaml

build:
	docker build -t ghcr.io/ajax-bakun-n/lab2-mcp-server:latest ./mcp-server

push:
	docker push ghcr.io/ajax-bakun-n/lab2-mcp-server:latest

clean:
	kubectl delete -k . --ignore-not-found
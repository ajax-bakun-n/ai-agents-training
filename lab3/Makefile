.PHONY: apply build push clean

apply:
	kubectl apply -f kagent/mcp-server.yaml
	kubectl apply -f kagent/agent.yaml

build:
	docker build -t ghcr.io/ajax-bakun-n/lab3-search-mcp:latest ./mcp-server

push:
	docker push ghcr.io/ajax-bakun-n/lab3-search-mcp:latest

clean:
	kubectl delete -f kagent/agent.yaml --ignore-not-found
	kubectl delete -f kagent/mcp-server.yaml --ignore-not-found
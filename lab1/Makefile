.PHONY: apply secrets standalone clean

# Create API key secrets manually before running apply.
# See README for instructions.

apply:
	kubectl apply -k .

standalone:
	env $$(grep -v '^#' .env | xargs) ~/.local/bin/agentgateway -f config.yaml

clean:
	kubectl delete -k . --ignore-not-found
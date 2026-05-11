.PHONY: setup apply standalone clean

setup:
	@test -f .env || (echo "copy .env.example to .env and fill in keys" && exit 1)
	@grep ANTHROPIC_API_KEY .env | sed 's/ANTHROPIC_API_KEY=/Authorization=/' > k8s/.anthropic.env
	@grep OPENAI_API_KEY .env | sed 's/OPENAI_API_KEY=/Authorization=/' > k8s/.openai.env

apply: setup
	kubectl apply -k .

standalone:
	env $$(grep -v '^#' .env | xargs) ~/.local/bin/agentgateway -f config.yaml

clean:
	rm -f k8s/.anthropic.env k8s/.openai.env
Deploying Basic Agentic Infrastructure:

Before deploying, create the required secrets manually:

  # agentgateway secrets (key must be named Authorization)
  kubectl create secret generic anthropic-secret \
    --from-literal=Authorization="Bearer <your-anthropic-api-key>" \
    --namespace agentgateway-system

  kubectl create secret generic openai-secret \
    --from-literal=Authorization="Bearer <your-openai-api-key>" \
    --namespace openai-system

  # kagent secret
  kubectl create secret generic anthropic-api-key \
    --from-literal=ANTHROPIC_API_KEY=<your-anthropic-api-key> \
    --namespace kagent

  # standalone agentgateway: export keys to environment
  export ANTHROPIC_API_KEY=<your-anthropic-api-key>
  export OPENAI_API_KEY=<your-openai-api-key>

Beginners:
1. Install agentgateway locally https://agentgateway.dev/docs/standalone/latest/deployment/binary/
2. Select llm provider https://agentgateway.dev/docs/standalone/latest/llm/providers/
3. Configure config.yaml https://agentgateway.dev/docs/standalone/latest/tutorials/llm-gateway/
4. Start gateway and access via UI http://localhost:15000/ui/
5. Verify access to llm and familiarize yourself with the fundamental capabilities of Backends and Policy

Experienced
1. Perform beginner tasks but as a helm deployment in a Kubernetes cluster
2. Create secrets manually (see above)
3. Deploy kagent https://kagent.dev/docs/kagent/getting-started/quickstart
4. Configure model route via agentgateway
5. Test the operation of any built-in agent

Max:
1. Perform tasks of experienced users with gateway API https://agentgateway.dev/docs/kubernetes/main/about/gateway-api/

Research-1: Evaluate the ADR of the S&T project: DevOps Bot/Agent
1. Your questions about the project, suggest improvements and solutions

Save the results of the work in your own GitHub repository.
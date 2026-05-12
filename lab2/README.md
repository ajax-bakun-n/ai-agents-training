MCP Tool Servers and Agents with Kagent

"abox" (agentbox) = agentgateway + kagent deployed together. Install once per cluster before starting any track.

Deploy abox:
  # Install agentgateway CRDs and proxy
  helm upgrade -i agentgateway-crds oci://cr.agentgateway.dev/charts/agentgateway-crds \
    --namespace agentgateway-system --create-namespace

  helm upgrade -i agentgateway oci://cr.agentgateway.dev/charts/agentgateway \
    --namespace agentgateway-system -f helm/values-agentgateway.yaml

  # Install kagent
  helm upgrade -i kagent oci://ghcr.io/kagent-dev/kagent/helm/kagent \
    --namespace kagent --create-namespace -f helm/values-kagent.yaml

Access UIs:
  # agentgateway UI  →  http://localhost:15000/ui/
  kubectl port-forward -n agentgateway-system svc/agentgateway 15000:9978

  # kagent UI  →  http://localhost:8080
  kubectl port-forward -n kagent svc/kagent-ui 8080:8080

  # Flux UI (if Flux is installed)  →  http://localhost:9001
  kubectl port-forward -n flux-system svc/weave-gitops 9001:9001

Beginners (завдання на сертифікат):
1. Deploy abox (see above)
2. Get access to the UIs: agentgateway, kagent, Flux (see above)
3. Copy .env.example to .env and fill in API keys
4. Apply model config, MCP tool server, and agent:
     make apply
5. Open kagent UI and test the k8s-assistant agent

Experienced:
1. Complete beginner tasks
2. Create the secret manually (required before Flux sync):
     make secret
3. Deploy GitOps resources to Flux:
     make gitops
4. Verify Flux reconciles the kagent resources:
     kubectl get kustomization -n flux-system lab2-kagent

Note: Flux Kustomization points to ./lab2/kagent in the repo. The secret must
exist in the kagent namespace before Flux deploys the Agent and ModelConfig.

Max:
Development:
1. Complete experienced tasks
2. Build and push the custom MCP server:
     make build && make push
3. Apply Max-track resources (custom MCPServer + agent):
     make apply-max
4. Watch KMCP controller deploy the MCP server pod:
     kubectl get pods -n kagent -w

Research: Preparation for MCP/A2A session
1. Complete the course: https://anthropic.skilljar.com/model-context-protocol-advanced-topics

Save the results of the work in your own GitHub repository.
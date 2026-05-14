MCP Sampling / Elicitation / MCP Apps

Beginners:

Research:
1. Identify real technical and business cases that can be implemented with
   MCP Sampling, Elicitation, or MCP Apps (choose one). Document findings
   and present at the session.

Development:
1. Learn kmcp https://www.solo.io/blog/introducing-kmcp
   Build and deploy your own MCP server using MCPServer CRD:
     make build && make push
     kubectl apply -f kagent/mcp-server.yaml
   Verify the server is deployed and tools are accessible via kagent UI.

2. Learn google-agents-cli https://google.github.io/agents-cli/
   Install: pip install google-agents-cli
   Configure and deploy your own agent that uses the MCP server above:
     agentcli deploy google-agents-cli/agent.yaml
   Test via the playground (see step 3).

3. Test your MCP server and agent:
     # Inspect MCP server tools interactively
     npx @modelcontextprotocol/inspector@0.21.1

     # Test agent via agents-cli playground
     agentcli playground

Experienced:
1. Complete beginner tasks
2. Development: Implement your own MCP Apps use case end-to-end

Max:
1. Complete experienced tasks
2. Development: Implement your own MCP Sampling or Elicitation use case

Save the results of the work in your own GitHub repository.
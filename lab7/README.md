Фінальна робота — Vin's Questions: Research & Evaluation of AI Infrastructure Setup

---

## 1. How could we handle "agent got stuck" scenarios?

Three layers of protection work well together.

At the gateway level, agentgateway lets you set a request timeout on the HTTPRoute — if a single
LLM call takes too long, it gets cancelled automatically. Inside the agent, kagent's `maxIterations`
field stops the loop after N tool-call rounds. For A2A tasks, a watchdog CronJob can poll
`tasks/get` and cancel anything that stays in `working` state too long.

Best practice: use gateway timeout as a hard limit, `maxIterations` as a soft limit, and a
Prometheus alert on task duration so you can see problems before users report them.

---

## 2. Any automatic timeout / circuit breaker patterns from the framework?

Yes, at multiple levels:

- **agentgateway** — `timeout` on HTTPRoute (per request) and BackendLBPolicy (per connection)
- **kgateway / Envoy** — `outlierDetection` in BackendTrafficPolicy: ejects a failing backend
  after N errors and brings it back after a cooldown period
- **kagent RemoteMCPServer** — `timeout` field for MCP tool calls (default 30s)
- **kagent Agent** — `maxIterations` to limit loop depth

No custom code needed, just configuration.

---

## 3. How does kgateway handle model failover?

kgateway is built on Envoy. You define multiple backends in one HTTPRoute — the primary gets
weight 100, standbys get weight 0. When the primary fails active health checks, Envoy shifts
traffic to the next backend automatically.

agentgateway normalises all provider APIs to the OpenAI format, so a failover from Anthropic to
OpenAI is invisible to the agent.

---

## 4. Can we automatically switch from OpenAI to Claude to a local model?

Yes. Configure three backends in agentgateway — Anthropic (weight 100), OpenAI (weight 0),
local vLLM (weight 0) — all behind one HTTPRoute with active health checks. Envoy moves traffic
down the list when a provider is unavailable.

One thing to keep in mind: kagent's ModelConfig points to one named backend. The automatic
failover has to happen inside agentgateway, not inside kagent. That way agents don't need to
know anything about it.

---

## 5. Could we seamlessly handle response formats from these providers?

Yes — agentgateway handles this. It translates every provider response into the OpenAI Chat
Completions format before the agent sees it. Anthropic uses different field names, different
role labels, different tool call structures — all of that gets normalised transparently.

From the agent's point of view, there is only one format regardless of which provider is active.
No code changes needed when switching providers.

---

## 6. Can we version the agents built with kagent?

There is no version field in the kagent Agent CRD, but Git + Kubernetes labels cover this well.

Every commit to your repository is a versioned snapshot — Flux reconciles whatever is in git.
You add a label like `app.kubernetes.io/version: "1.2.0"` for tracking. To run two versions at
the same time, deploy them as separate Agent CRDs (`k8s-assistant-v1`, `k8s-assistant-v2`) and
route between them at the gateway.

The key habit: name ConfigMaps with a content hash so rollback is always just `git revert`.

---

## 7. Any blue/green or canary deployment patterns for agents?

Yes — agents are standard Kubernetes workloads behind a Gateway API HTTPRoute, so normal
progressive delivery patterns work as-is.

Canary: split traffic by weight between two backend services and shift gradually.

```yaml
backendRefs:
  - name: agent-v1-svc
    weight: 90
  - name: agent-v2-svc
    weight: 10
```

Blue/green: route requests with `X-Agent-Version: v2` header to the new version only, keeping
production untouched. Flagger can automate weight shifting and rollback based on Prometheus
metrics (error rate, latency).

---

## 8. What is the FastMCP Python framework?

FastMCP is the official high-level Python library for building MCP servers. It comes with the
`mcp` package and makes building tools very simple — you just write a function with a decorator:

```python
from mcp.server.fastmcp import FastMCP

app = FastMCP("my-server")

@app.tool()
def fetch_url(url: str) -> str:
    """Fetch the contents of a URL."""
    import httpx
    return httpx.get(url).text

app.run(transport="streamable-http", host="0.0.0.0", port=8080)
```

The JSON schema is generated automatically from type hints and docstrings. It supports tools,
resources, and prompts, and works with async functions. We used it in labs 3 and 5.

---

## 9. Is it the easiest path to MCP?

For Python — yes.

The fastest way to prototype is to embed FastMCP code in a kagent ConfigMap (lab3 pattern): no
Docker build, no image registry, just edit a YAML field and `kubectl apply`. The trade-off is
cold-start time because `pip install` runs on every pod start.

For stable tools, a proper container image (lab5 pattern) is still simple and more reliable.
The Go MCP SDK (lab2) needs more boilerplate but gives better performance and type safety.

FastMCP is the right default. Reach for Go when you have a specific reason.

---

## 10. About FinOps: how much control can I have?

Honestly — good visibility today, limited enforcement out of the box.

**What works now:**
- Provider-side spending caps (OpenAI and Anthropic both support this per API key)
- agentgateway RateLimitPolicy — but it limits request count, not token count
- Phoenix (lab5) shows token usage per trace using OpenTelemetry Gen AI conventions
- Kubernetes ResourceQuota limits CPU/memory for agent workloads

**What requires custom work:**
- Blocking an agent when it hits a token budget — not natively supported in agentgateway or
  kagent today. You need to build it (see Q12).

---

## 11. Token level / per agent level

agentgateway emits standard OpenTelemetry metrics: `gen_ai.usage.input_tokens` and
`gen_ai.usage.output_tokens`. You can query these in Prometheus per agent by adding agent
identity as a label.

Phoenix makes it more visual — every request is a trace with token counts attached, and you
filter by `service.name` or any other attribute to see per-agent consumption.

The gap: you can *see* that an agent used 2M tokens today, but nothing in the stack
automatically throttles it based on that number.

---

## 12. Can I implement custom cost controls?

Yes. The cleanest approach is Envoy's external authorisation (ext-authz) extension point: a
small gRPC service that intercepts every LLM request, counts tokens with `tiktoken`, checks a
budget store (Redis), and returns allow or deny. kgateway wires it in via BackendTrafficPolicy.
The agent is blocked at the gateway — no provider call happens.

A simpler but weaker approach: expose a `check_budget(agent_id)` MCP tool. The agent calls it
before expensive operations. Easy to build, but not enforceable — the model can choose to skip
it.

For real cost control, the ext-authz approach is the right one.

---

## 13. Per-agent budgets or depth of token limits

**Iteration depth** — kagent's `maxIterations` in the Agent spec caps how many tool-call rounds
the agent can make per task. Simple and built-in.

**Token budget per agent** — not built-in. Use the ext-authz pattern (Q12) with a budget store
keyed by agent name. Set a daily limit per agent, alert at 80%, hard block at 100%.

**Max tokens per call** — set `max_tokens` in the agentgateway backend transformation config or
in the agent's system prompt. No external state needed.

---

## 14. vLLM suitable for agents with many tool calls, or better for single-shot inference?

vLLM was designed for high-throughput single-shot inference and is excellent at it. For agents
with many back-and-forth tool calls, it still works but needs specific configuration.

The problem: each tool-call round trip is a separate request. Without prefix caching, the
growing conversation history is reprocessed from scratch every time, so latency grows with the
number of turns.

The fix: enable `--enable-prefix-caching` and set up session affinity (route each agent session
to the same vLLM replica). Then only new tokens are computed per turn, and latency stays roughly
constant regardless of conversation length.

Without these settings — not ideal for agents. With them — works well.

---

## 15. llm-d's scheduler — helps when agents make 15 LLM calls?

Yes, significantly. llm-d was built exactly for this.

The key feature is prefix-aware routing. llm-d knows which KV-cache content each vLLM replica
holds. When an agent makes its 5th or 10th call in a session, llm-d routes it to the replica
that already has the full conversation history cached — so only the new tokens are computed.

A standard load balancer scatters requests randomly across replicas. Every call is a cache miss.
Every call re-processes the growing history. Latency grows with conversation depth.

With llm-d, turns 2 through 15 are much faster than turn 1. The longer the conversation, the
bigger the benefit over random load balancing. For a 15-call agent task, the total latency
reduction can be 40–60%.

llm-d also supports separating prefill (first token computation) and decode (token generation)
onto different GPU pools, which helps further for long-context agentic sessions.

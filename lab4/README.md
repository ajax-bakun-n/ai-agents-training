A2A Protocol — Agent-to-Agent Communication

Початківці (завдання на сертифікат)

Research:
1. Ознайомитися із специфікацією A2A https://a2a-protocol.org
   Вивчити структуру Agent Card, Well-Known URI, формат задач (tasks/send, tasks/get).

Development:
2. Реалізувати власного агента (будь-який фреймворк) з Agent Card
   та отримати картку агента за Well-Known URI:
     curl http://<agent-host>/.well-known/agent.json
   Приклад реалізації: agent/main.py
   Розгорнути в кластері:
     kubectl apply -f k8s/a2a-agent.yaml

Infrastructure:
3. Розгорнути Inventory на abox (або будь-яку альтернативу, можна на власному середовищі)
   та отримати перелік AI ресурсів в кластері:
     # Inventory через kagent API
     kubectl get agents,mcpservers,remotemcpservers,modelconfigs -A
     # або через kagent UI → http://localhost:18080

4. Розгорнути MCPG (MCP Gateway) у власній AI Інфраструктурі або аналогічний інструмент.
   agentgateway вже виконує роль MCP Gateway — перевірити конфігурацію:
     kubectl get httproute,backendlbpolicies -n agentgateway-system
   Альтернатива: https://github.com/modelcontextprotocol/mcpgateway

5. Розгорнути векторну базу даних Qdrant https://github.com/qdrant/qdrant-helm
   в abox або на власному середовищі:
     kubectl apply -f k8s/qdrant.yaml
   Перевірити доступність:
     kubectl port-forward svc/qdrant 6333:6333
     curl http://localhost:6333/healthz

Досвідчені
1. Завдання початківців
2. Development: Реалізувати A2A task комунікацію між двома агентами
   — один агент надсилає завдання другому через tasks/send
   — перевірити статус виконання через tasks/get
   Приклад: agent/orchestrator.py

Макс
1. Завдання досвідчених
2. Development: Реалізувати A2A team з власним агентом та агентами kagent (на власний вибір)
   і поставити одне завдання на виконання різними агентами комплексно.
   — власний агент як оркестратор
   — kagent агенти як виконавці (k8s-assistant, k8s-research-agent)
   — спільний контекст через sessionId

*результат завдання можна здавати у форматі asciinema з посиланням на публічний запис
 (не сам файл запису)

Save the results of the work in your own GitHub repository.
MCP Sampling / Elicitation / MCP Apps

Початківці (завдання на сертифікат)

Research:
1. Ознайомитися з реальними технічними та бізнес-кейсами, де застосовуються
   MCP Sampling, Elicitation або MCP Apps (обрати один). Задокументувати висновки
   та представити на сесії.

Development:
2. Навчитися kmcp https://www.solo.io/blog/introducing-kmcp
   Розгорнути MCP сервер (Python FastMCP + DuckDuckGo, без API ключа):
     kubectl apply -f kagent/mcp-server.yaml
   Переконатись що сервер розгорнуто і інструменти доступні в kagent UI.

3. Навчитися google-agents-cli https://google.github.io/agents-cli/
   Встановити: pip install google-agents-cli
   Налаштувати та розгорнути власного агента:
     agentcli deploy google-agents-cli/agent.yaml
   Протестувати через playground (крок 4).

4. Протестувати MCP сервер та агента:
     # Переглянути інструменти MCP сервера інтерактивно
     npx @modelcontextprotocol/inspector@0.21.1

     # Протестувати агента через playground
     agentcli playground

Досвідчені
1. Завдання початківців
2. Development: Реалізувати власний end-to-end кейс MCP Apps

Макс
1. Завдання досвідчених
2. Development: Реалізувати власний кейс MCP Sampling або Elicitation

Save the results of the work in your own GitHub repository.
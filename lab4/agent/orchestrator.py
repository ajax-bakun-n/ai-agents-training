"""
Orchestrator: sends a task to another A2A agent and returns the result.
Usage: python orchestrator.py <agent-url> <message>
"""
import sys
import uuid
import httpx


def send_task(agent_url: str, text: str) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tasks/send",
        "params": {
            "id": str(uuid.uuid4()),
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": text}],
            },
        },
    }
    r = httpx.post(agent_url, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


def get_task(agent_url: str, task_id: str) -> dict:
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tasks/get",
        "params": {"id": task_id},
    }
    r = httpx.post(agent_url, json=payload, timeout=10)
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    message = sys.argv[2] if len(sys.argv) > 2 else "Hello from orchestrator!"

    print(f"Sending task to {url} ...")
    result = send_task(url, message)
    print("Response:", result)

    task_id = result.get("result", {}).get("id")
    if task_id:
        status = get_task(url, task_id)
        print("Task status:", status)
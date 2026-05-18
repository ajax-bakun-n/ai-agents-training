"""
Minimal A2A-compliant agent.
- Serves Agent Card at GET /.well-known/agent.json
- Handles JSON-RPC 2.0 tasks at POST /
"""
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="A2A Agent")

AGENT_URL = "http://a2a-agent.kagent.svc.cluster.local:8080"

AGENT_CARD = {
    "name": "Lab4 A2A Agent",
    "description": "Example A2A agent that echoes tasks back to the caller",
    "url": AGENT_URL,
    "version": "1.0.0",
    "documentationUrl": "https://a2a-protocol.org",
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
        "stateTransitionHistory": True,
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [
        {
            "id": "echo",
            "name": "Echo",
            "description": "Echoes the input text back",
            "tags": ["demo"],
            "examples": ["Hello, agent!"],
        }
    ],
}


@app.get("/.well-known/agent.json")
async def agent_card():
    return AGENT_CARD


@app.post("/")
async def handle_rpc(request: Request):
    body = await request.json()
    method = body.get("method", "")
    params = body.get("params", {})
    req_id = body.get("id")

    if method == "tasks/send":
        task_id = params.get("id") or str(uuid.uuid4())
        message = params.get("message", {})
        text = next(
            (p["text"] for p in message.get("parts", []) if p.get("type") == "text"),
            "",
        )
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "id": task_id,
                "status": {
                    "state": "completed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
                "artifacts": [
                    {
                        "parts": [{"type": "text", "text": f"Echo: {text}"}],
                        "index": 0,
                    }
                ],
            },
        }

    if method == "tasks/get":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32001, "message": "Task not found"},
        }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"},
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
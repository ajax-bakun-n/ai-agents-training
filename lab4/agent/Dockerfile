FROM python:3.12-slim
RUN pip install --no-cache-dir fastapi uvicorn httpx
WORKDIR /app
COPY main.py orchestrator.py ./
CMD ["python", "main.py"]
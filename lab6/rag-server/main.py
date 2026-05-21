import os
import uuid
import google.generativeai as genai
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from mcp.server.fastmcp import FastMCP

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
COLLECTION = "knowledge_base"
EMBEDDING_DIM = 768  # text-embedding-004

genai.configure(api_key=GEMINI_API_KEY)
qdrant = QdrantClient(url=QDRANT_URL)

app = FastMCP("rag-tools")


def _embedding(text: str) -> list:
    return genai.embed_content(model="models/text-embedding-004", content=text)["embedding"]


def _ensure_collection():
    names = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION not in names:
        qdrant.create_collection(
            COLLECTION,
            vectors_config=VectorParams(size=EMBEDDING_DIM, distance=Distance.COSINE),
        )


@app.tool()
def ingest_document(content: str, source: str = "manual") -> str:
    """Ingest a document into the knowledge base"""
    _ensure_collection()
    qdrant.upsert(
        collection_name=COLLECTION,
        points=[PointStruct(
            id=str(uuid.uuid4()),
            vector=_embedding(content),
            payload={"content": content, "source": source},
        )],
    )
    return f"Ingested document from source '{source}'"


@app.tool()
def search_knowledge_base(query: str, top_k: int = 3) -> str:
    """Search the knowledge base for relevant documents"""
    _ensure_collection()
    results = qdrant.search(
        collection_name=COLLECTION,
        query_vector=_embedding(query),
        limit=top_k,
    )
    if not results:
        return "No relevant documents found."
    return "\n\n".join(
        f"[score={r.score:.3f}] {r.payload.get('content', '')}" for r in results
    )


if __name__ == "__main__":
    app.run(transport="streamable-http", host="0.0.0.0", port=8080)

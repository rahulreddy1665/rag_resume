import os
from qdrant_client import QdrantClient
from embed import embed_texts

COLLECTION = "resume"
client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

def retrieve(question, top_k=4):
    q_vector = embed_texts([question], "RETRIEVAL_QUERY")[0]
    results = client.query_points(
        collection_name=COLLECTION,
        query=q_vector.tolist(),
        limit=top_k,
    ).points
    return [{"score": r.score, "text": r.payload["text"]} for r in results]

if __name__ == "__main__":
    questions = [
        "What programming languages does he know?",
        "What did he do at JNET Technologies?",
        "Has he worked on AI chatbots?",
        "Where did he study?",
        "What projects has he built?",
    ]
    for q in questions:
        print(f"\n=== {q} ===")
        for r in retrieve(q):
            print(f"{r['score']:.3f}  {r['text'][:100]} ...")
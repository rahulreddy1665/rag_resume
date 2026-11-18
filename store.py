import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from load import load_resume
from chunk import chunk_by_section
from embed import embed_texts

COLLECTION = "resume"
client = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY"),
)
def store_chunks(chunks, vectors):
    if client.collection_exists(COLLECTION):
        client.delete_collection(COLLECTION)

    client.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=vectors.shape[1], distance=Distance.COSINE),
    )

    points = [
        PointStruct(id=i, vector=vectors[i].tolist(), payload={"text": chunks[i]})
        for i in range(len(chunks))
    ]
    client.upsert(collection_name=COLLECTION, points=points)
if __name__ == "__main__":
    chunks = chunk_by_section(load_resume("resume.pdf"))
    vectors = embed_texts(chunks, "RETRIEVAL_DOCUMENT")
    store_chunks(chunks, vectors)
    print("Stored:", client.count(COLLECTION).count, "points")
import os
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types
from load import load_resume
from chunk import chunk_by_section



load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def embed_texts(texts, task_type):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=768,
        ),
    )
    vectors = np.array([e.values for e in result.embeddings])
    return vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

if __name__ == "__main__":
    chunks = chunk_by_section(load_resume("resume.pdf"))
    chunk_vectors = embed_texts(chunks, "RETRIEVAL_DOCUMENT")
    print("Shape:", chunk_vectors.shape)
    print("First 5 numbers of chunk 0:", chunk_vectors[0][:5])

    # question = "What programming languages does he know?"
    # q_vector = embed_texts([question], "RETRIEVAL_QUERY")[0]

    question = "What projects has he built?"
    q_vector = embed_texts([question], "RETRIEVAL_QUERY")[0]

    scores = chunk_vectors @ q_vector
    best = scores.argsort()[::-1]

    print(f"\nQuestion: {question}")
    for i in best:
        print(f"\nChunk {i} (score {scores[i]:.3f}):")
        print(chunks[i][:200], "...")
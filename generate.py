from google.genai import types
from embed import client
from retrieve import retrieve
from google.genai import errors


MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash", "gemini-2.5-flash-lite"]

SYSTEM_PROMPT = """You are a helpful assistant on Rahul Reddy's portfolio website, answering visitors' questions about Rahul.

Rules:
- Answer using ONLY the information in the provided context. Never guess or invent details.
- If the context does not contain the answer, say you don't have that information, and suggest reaching out via email at rahulreddy1665@gmail.com or LinkedIn.
- Only suggest contacting Rahul when you cannot answer. Do not add it to answers you can give.
- Never mention "context", "excerpts", "documents" or "the resume" in your answer; speak naturally, as if you simply know about Rahul.
- Keep answers short, friendly and professional. Use bullet points only for lists of 3 or more items.
- For broad questions, summarize the 3–5 most important highlights, then offer to go into more detail on any of them.
- Refer to Rahul in the third person."""

def answer(question, top_k=4):
    chunks = retrieve(question, top_k)
    context = "\n\n".join(f"[{i+1}] {c['text']}" for i, c in enumerate(chunks))
    prompt = f"Resume excerpts:\n{context}\n\nQuestion: {question}"

    for model in MODELS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.2,
                ),
            )
            return response.text, chunks
        except errors.ServerError:
            print(f"{model} unavailable, trying next model...")
    return "Sorry, the assistant is busy right now. Please try again shortly.", chunks
    return response.text, chunks

if __name__ == "__main__":
    questions = [
        "What programming languages does he know?",
        "What did he do at Agilets?",
        "Where did he study?",
        "What is his current salary?",
        "Does he have experience with Kubernetes?",
    ]
    for q in questions:
        text, chunks = answer(q)
        print(f"\n=== {q} ===\n{text}")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from generate import answer
import os

app = FastAPI(title="Resume RAG API")

origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
class Question(BaseModel):
    question: str = Field(min_length=1, max_length=300)
    @app.get("/")
    def health():
      return {"status": "ok"}


@app.post("/ask")
def ask(body: Question):
    text, chunks = answer(body.question)
    return {"answer": text, "sources": [c["text"] for c in chunks]}
import os
from sentence_transformers import CrossEncoder
from dotenv import load_dotenv

load_dotenv()

RERANKER_MODEL = os.getenv("RERANKER_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
TOP_K_RERANK = int(os.getenv("TOP_K_RERANK", 3))

class Reranker:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = CrossEncoder(RERANKER_MODEL)
        return cls._instance
    
    def rerank(self, query: str, candidates: list[dict], top_k: int = TOP_K_RERANK) -> list[dict]:
        if not candidates:
            return []
        pairs = [(query, candidate["text"]) for candidate in candidates]
        scores = self.model.predict(pairs)
        for i, candidate in enumerate(candidates):
            candidate["rerank_score"] = float(scores[i])
        reranked = sorted(candidates, key=lambda x: x["rerank_score"], reverse=True)
        return reranked[:top_k]
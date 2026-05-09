import os
import pickle
import logging
import numpy as np
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv

load_dotenv()

BM25_INDEX_PATH = os.getenv("BM25_INDEX_PATH", "./bm25_index.pkl")
logger = logging.getLogger(__name__)

def _tokenize(text: str) -> list[str]:
    return text.lower().split()

class BM25Store:
    def __init__(self):
        self.index = None
        self.chunks = []
        self._load_if_exists()
    
    def _load_if_exists(self):
        if os.path.exists(BM25_INDEX_PATH):
            try:
                with open(BM25_INDEX_PATH, "rb") as f:
                    data = pickle.load(f)
                    self.index = data["index"]
                    self.chunks = data["chunks"]
            except Exception as e:
                logger.warning(f"Could not load BM25 index: {e}")
    
    def build_index(self, texts: list[str], chunks: list[dict]):
        tokenized = [_tokenize(t) for t in texts]
        self.index = BM25Okapi(tokenized)
        self.chunks = chunks
        with open(BM25_INDEX_PATH, "wb") as f:
            pickle.dump({"index": self.index, "chunks": self.chunks}, f)
    
    def query(self, query: str, top_k: int = 10) -> list[dict]:
        if self.index is None or not self.chunks:
            return []
        
        tokenized_query = _tokenize(query)
        scores = self.index.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if scores[idx] <= 0:
                continue
            chunk = self.chunks[idx]
            results.append({
                "text": chunk.get("parent_text", chunk.get("text", "")),
                "metadata": {
                    "source_file": chunk.get("source_file", ""),
                    "section_heading": chunk.get("section_heading", ""),
                    "doc_type": chunk.get("doc_type", ""),
                    "page_number": str(chunk.get("page_number", "")),
                    "chunk_index": str(chunk.get("chunk_position", idx))
                },
                "score": float(scores[idx]),
                "id": f"bm25_{idx}"
            })
        return results
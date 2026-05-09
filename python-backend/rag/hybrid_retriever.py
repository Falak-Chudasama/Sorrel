from rag.chroma_store import ChromaStore
from rag.bm25_store import BM25Store
from rag.embedder import Embedder
import os
from dotenv import load_dotenv

load_dotenv()
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", 10))
RRF_K = 60

def reciprocal_rank_fusion(dense_results: list[dict], sparse_results: list[dict], k: int = RRF_K) -> list[dict]:
    rrf_scores = {}
    doc_map = {}
    
    def _get_doc_key(result: dict) -> str:
        meta = result.get("metadata", {})
        return f"{meta.get('source_file', '')}::{meta.get('chunk_index', result.get('id', ''))}"
    
    for rank, result in enumerate(dense_results):
        doc_key = _get_doc_key(result)
        rrf_scores[doc_key] = rrf_scores.get(doc_key, 0) + 1 / (k + rank + 1)
        if doc_key not in doc_map:
            doc_map[doc_key] = result
            
    for rank, result in enumerate(sparse_results):
        doc_key = _get_doc_key(result)
        rrf_scores[doc_key] = rrf_scores.get(doc_key, 0) + 1 / (k + rank + 1)
        if doc_key not in doc_map:
            doc_map[doc_key] = result
            
    sorted_keys = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)
    merged = []
    for key in sorted_keys:
        doc = doc_map[key].copy()
        doc["rrf_score"] = rrf_scores[key]
        merged.append(doc)
    return merged

class HybridRetriever:
    def __init__(self):
        self.embedder = Embedder()
        self.chroma_store = ChromaStore()
        self.bm25_store = BM25Store()
    
    def retrieve(self, query: str, top_k: int = TOP_K_RETRIEVAL) -> list[dict]:
        query_embedding = self.embedder.embed_query(query)
        dense_results = self.chroma_store.query_hero(query_embedding, top_k=top_k)
        sparse_results = self.bm25_store.query(query, top_k=top_k)
        return reciprocal_rank_fusion(dense_results, sparse_results)[:top_k]
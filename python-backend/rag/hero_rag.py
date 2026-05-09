from rag.hybrid_retriever import HybridRetriever
from rag.reranker import Reranker
import os
from dotenv import load_dotenv

load_dotenv()

TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", 10))
TOP_K_RERANK = int(os.getenv("TOP_K_RERANK", 3))

class HeroRAG:
    def __init__(self):
        self.retriever = HybridRetriever()
        self.reranker = Reranker()
    
    def query(self, user_query: str) -> dict:
        candidates = self.retriever.retrieve(user_query, top_k=TOP_K_RETRIEVAL)
        if not candidates:
            return {"context_text": "", "sources": [], "chunks": []}
        
        top_chunks = self.reranker.rerank(user_query, candidates, top_k=TOP_K_RERANK)
        context_parts = []
        sources = []
        for i, chunk in enumerate(top_chunks):
            meta = chunk.get("metadata", {})
            source_file = meta.get("source_file", "Unknown Source")
            section_heading = meta.get("section_heading", "")
            page_number = meta.get("page_number", "")
            context_block = (f"--- SOURCE {i+1}: {source_file}" + (f", Section: {section_heading}" if section_heading else "") + (f", Page: {page_number}" if page_number else "") + f" ---\n{chunk['text']}\n")
            context_parts.append(context_block)
            sources.append({"source_file": source_file, "section_heading": section_heading, "page_number": page_number, "relevance_score": round(chunk.get("rerank_score", 0), 4)})
            
        return {"context_text": "\n".join(context_parts), "sources": sources, "chunks": top_chunks}
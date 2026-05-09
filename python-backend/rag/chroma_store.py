import os
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chromadb_store")
HERO_COLLECTION = os.getenv("HERO_COLLECTION", "hero_rag")
CHAT_COLLECTION = os.getenv("CHAT_COLLECTION", "chat_rag")

class ChromaStore:
    _client = None
    
    def __init__(self):
        if ChromaStore._client is None:
            ChromaStore._client = chromadb.PersistentClient(
                path=CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
        self.client = ChromaStore._client
    
    def upsert_hero_chunks(self, chunks: list[dict], embeddings: list[list[float]]):
        try:
            self.client.delete_collection(HERO_COLLECTION)
        except Exception:
            pass
        
        collection = self.client.get_or_create_collection(
            name=HERO_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        documents = [chunk["parent_text"] for chunk in chunks]
        metadatas = [
            {
                "source_file": chunk["source_file"],
                "section_heading": chunk["section_heading"],
                "doc_type": chunk["doc_type"],
                "page_number": str(chunk.get("page_number", "")),
                "chunk_index": str(chunk.get("chunk_position", i)),
                "child_text": chunk["text"]
            }
            for i, chunk in enumerate(chunks)
        ]
        
        batch_size = 500
        for start in range(0, len(chunks), batch_size):
            end = start + batch_size
            collection.upsert(
                ids=ids[start:end],
                documents=documents[start:end],
                embeddings=embeddings[start:end],
                metadatas=metadatas[start:end]
            )
    
    def query_hero(self, query_embedding: list[float], top_k: int = 10) -> list[dict]:
        collection = self.client.get_or_create_collection(
            name=HERO_COLLECTION,
            metadata={"hnsw:space": "cosine"}
        )
        
        # FIX: Check if database is empty first
        count = collection.count()
        if count == 0:
            return []
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, count),
            include=["documents", "metadatas", "distances"]
        )
        
        if not results["documents"] or not results["documents"][0]:
            return []
        
        formatted = []
        for i, doc in enumerate(results["documents"][0]):
            formatted.append({
                "text": doc,
                "metadata": results["metadatas"][0][i],
                "score": 1 - results["distances"][0][i],
                "id": results["ids"][0][i] if "ids" in results else f"result_{i}"
            })
        
        return formatted
    
    def _get_chat_collection(self, session_id: str):
        return self.client.get_or_create_collection(
            name=f"{CHAT_COLLECTION}_{session_id}",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_chat_turn(self, session_id: str, turn_id: str, text: str, embedding: list[float], role: str):
        collection = self._get_chat_collection(session_id)
        collection.upsert(
            ids=[turn_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{"role": role, "session_id": session_id}]
        )
    
    def query_chat(self, session_id: str, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        collection = self._get_chat_collection(session_id)
        count = collection.count()
        if count == 0:
            return []
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, count),
            include=["documents", "metadatas", "distances"]
        )
        
        if not results["documents"] or not results["documents"][0]:
            return []
        
        return [
            {
                "text": doc,
                "metadata": results["metadatas"][0][i],
                "score": 1 - results["distances"][0][i]
            }
            for i, doc in enumerate(results["documents"][0])
        ]
    
    def clear_chat_session(self, session_id: str):
        try:
            self.client.delete_collection(f"{CHAT_COLLECTION}_{session_id}")
        except Exception:
            pass
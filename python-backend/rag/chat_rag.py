import uuid
from rag.chroma_store import ChromaStore
from rag.embedder import Embedder

class ChatRAG:
    def __init__(self):
        self.chroma_store = ChromaStore()
        self.embedder = Embedder()
    
    def store_turn(self, session_id: str, role: str, content: str):
        turn_id = str(uuid.uuid4())
        text = f"[{role}]: {content}"
        embedding = self.embedder.embed_single(text)
        self.chroma_store.add_chat_turn(session_id, turn_id, text, embedding, role)
    
    def get_context(self, session_id: str, current_query: str, top_k: int = 5) -> str:
        query_embedding = self.embedder.embed_query(current_query)
        turns = self.chroma_store.query_chat(session_id, query_embedding, top_k=top_k)
        if not turns:
            return ""
        turns_sorted = sorted(turns, key=lambda t: t["score"], reverse=True)
        return "\n".join([turn["text"] for turn in turns_sorted])
    
    def clear_session(self, session_id: str):
        self.chroma_store.clear_chat_session(session_id)
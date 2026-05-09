import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-large-en-v1.5")
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

class Embedder:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = SentenceTransformer(EMBED_MODEL)
        return cls._instance
    
    def embed_query(self, query: str) -> list[float]:
        prefixed = QUERY_PREFIX + query
        embedding = self.model.encode(prefixed, normalize_embeddings=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, normalize_embeddings=True, batch_size=32, show_progress_bar=True)
        return embeddings.tolist()
    
    def embed_single(self, text: str) -> list[float]:
        embedding = self.model.encode(text, normalize_embeddings=True)
        return embedding.tolist()
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from ingestion.loader import load_document
from ingestion.chunker import chunk_sections
from rag.embedder import Embedder
from rag.chroma_store import ChromaStore
from rag.bm25_store import BM25Store

load_dotenv()
logger = logging.getLogger(__name__)

POOL_DIR = os.getenv("POOL_DIR", "../pool")
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx"}

def run_ingestion():
    pool_path = Path(POOL_DIR)
    if not pool_path.exists():
        pool_path.mkdir(parents=True, exist_ok=True)
        return
    
    files = [f for f in pool_path.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS]
    if not files:
        return
        
    embedder = Embedder()
    chroma_store = ChromaStore()
    bm25_store = BM25Store()
    all_chunks = []
    
    for file_path in files:
        try:
            sections = load_document(str(file_path))
            chunks = chunk_sections(sections)
            all_chunks.extend(chunks)
        except Exception as e:
            logger.error(f"Failed to process {file_path.name}: {e}")
            continue
            
    if not all_chunks:
        return
        
    texts_to_embed = [chunk["enriched_text"] for chunk in all_chunks]
    embeddings = embedder.embed_batch(texts_to_embed)
    chroma_store.upsert_hero_chunks(all_chunks, embeddings)
    
    raw_texts = [chunk["text"] for chunk in all_chunks]
    bm25_store.build_index(raw_texts, all_chunks)
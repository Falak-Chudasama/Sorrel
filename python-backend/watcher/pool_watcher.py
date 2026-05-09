import time
import threading
import logging
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ingestion.pipeline import run_ingestion
from dotenv import load_dotenv

load_dotenv()

POOL_DIR = os.getenv("POOL_DIR", "../pool")
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx"}
DEBOUNCE_SECONDS = 3

logger = logging.getLogger(__name__)

class PoolEventHandler(FileSystemEventHandler):
    def __init__(self):
        self._timer = None
        self._lock = threading.Lock()
    
    def _is_supported(self, path: str) -> bool:
        from pathlib import Path
        return Path(path).suffix.lower() in SUPPORTED_EXTENSIONS
    
    def _debounced_ingest(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(DEBOUNCE_SECONDS, self._run_ingest)
            self._timer.start()
    
    def _run_ingest(self):
        try:
            run_ingestion()
        except Exception as e:
            logger.error(f"Re-ingestion failed: {e}")
    
    def on_created(self, event):
        if not event.is_directory and self._is_supported(event.src_path):
            self._debounced_ingest()
    
    def on_modified(self, event):
        if not event.is_directory and self._is_supported(event.src_path):
            self._debounced_ingest()
    
    def on_deleted(self, event):
        if not event.is_directory and self._is_supported(event.src_path):
            self._debounced_ingest()

def start_watcher():
    event_handler = PoolEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path=POOL_DIR, recursive=False)
    observer.start()
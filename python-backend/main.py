import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from ingestion.pipeline import run_ingestion
from watcher.pool_watcher import start_watcher
from contextlib import asynccontextmanager

# Enhanced logging with timestamps and line numbers
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up... Running ingestion and watchers.")
    run_ingestion()
    start_watcher()
    yield
    logger.info("Shutting down...")

app = FastAPI(title="Academic Chatbot API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")
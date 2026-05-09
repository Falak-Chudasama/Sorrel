from fastapi import APIRouter, HTTPException
from api.schemas import ChatRequest, ChatResponse, IngestResponse, SourceCitation
from rag.hero_rag import HeroRAG
from rag.chat_rag import ChatRAG
from llm.groq_client import GroqClient
from llm.prompt_builder import build_prompt
from ingestion.pipeline import run_ingestion
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

hero_rag = HeroRAG()
chat_rag = ChatRAG()
groq_client = GroqClient()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id = request.session_id
        user_message = request.message.strip()
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
        hero_result = hero_rag.query(user_message)
        hero_context = hero_result["context_text"]
        sources = hero_result["sources"]
        
        chat_history = chat_rag.get_context(session_id, user_message, top_k=5)
        
        messages = build_prompt(user_query=user_message, hero_context=hero_context, chat_history=chat_history)
        response_text = groq_client.generate(messages)
        
        chat_rag.store_turn(session_id, "user", user_message)
        chat_rag.store_turn(session_id, "assistant", response_text)
        
        return ChatResponse(
            session_id=session_id,
            response=response_text,
            sources=[SourceCitation(**s) for s in sources]
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest", response_model=IngestResponse)
async def ingest():
    try:
        run_ingestion()
        return IngestResponse(status="success", message="Ingestion completed successfully.")
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    chat_rag.clear_session(session_id)
    return {"status": "cleared", "session_id": session_id}

@router.get("/health")
async def health():
    return {"status": "ok", "model": "bge-large-en-v1.5"}
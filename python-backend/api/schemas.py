from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    session_id: str
    message: str

class SourceCitation(BaseModel):
    source_file: str
    section_heading: str
    page_number: Optional[str] = None
    relevance_score: Optional[float] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str
    sources: list[SourceCitation]

class IngestResponse(BaseModel):
    status: str
    message: str
    chunks_processed: Optional[int] = None
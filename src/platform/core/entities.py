from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    
class SearchResult(BaseModel):
    title: str
    content: str
    source_url: str
    score: float 
    
class AgentState(BaseModel):
    """The central state for Agentic workflow"""
    session_id: str
    messages: List[Message] = []
    context_data: List[SearchResult] = []
    next_step: Optional[str] = None
    metadata: Dict[str, Any] = {}
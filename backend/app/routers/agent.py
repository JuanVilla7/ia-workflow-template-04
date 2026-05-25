import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.agent import ChatRequest, ChatResponse
from app.services.agent import agent

logger = logging.getLogger("api.routers.agent")

router = APIRouter(prefix="/agent", tags=["agent"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    logger.info("POST /agent/chat message=%s", request.message)
    try:
        result = await agent.run(request.message, deps=db)
        return ChatResponse(response=result.output)
    except Exception as e:
        logger.error("Agent error: %s", str(e), exc_info=True)
        return ChatResponse(response=f"I encountered an error while processing your request: {str(e)}")

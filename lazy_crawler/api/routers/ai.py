from fastapi import APIRouter, Depends, HTTPException, Body
from lazy_crawler.api.database import User
from lazy_crawler.api.auth import get_current_user
from lazy_crawler.api.services.ai_service import chat_with_data, generate_chart_config
from pydantic import BaseModel

router = APIRouter(prefix="/api/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str
    context: str = ""


class ChartRequest(BaseModel):
    description: str
    data_summary: str = ""


@router.post("/chat")
async def ai_chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    response = await chat_with_data(request.message, request.context)
    return {"response": response}


@router.post("/chart")
async def ai_chart(
    request: ChartRequest, current_user: User = Depends(get_current_user)
):
    config = await generate_chart_config(request.description, request.data_summary)
    return config

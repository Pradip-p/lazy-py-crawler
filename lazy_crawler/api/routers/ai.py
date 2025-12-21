from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import StreamingResponse
from lazy_crawler.api.database import User
from lazy_crawler.api.auth import get_current_user
from lazy_crawler.api.services.ai_service import chat_with_data, generate_chart_config
from lazy_crawler.api.services.ollama_service import (
    chat_with_ollama,
    chat_stream_ollama,
    list_available_models,
    check_ollama_health,
    answer_question,
    generate_summary,
    OllamaError,
)
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ai", tags=["ai"])


class ChatRequest(BaseModel):
    message: str
    context: str = ""


class OllamaChatRequest(BaseModel):
    prompt: str
    model: str = "qwen2.5:0.5b"
    temperature: float = 0.7
    top_p: float = 0.9
    stream: bool = False


class ChartRequest(BaseModel):
    description: str
    data_summary: str = ""


class SummaryRequest(BaseModel):
    text: str
    max_length: int = 150


@router.post("/chat")
async def ai_chat(
    request: ChatRequest,
    #   current_user: User = Depends(get_current_user)
):
    """Chat using Google Gemini AI (requires API key)"""
    response = await chat_with_data(request.message, request.context)
    return {"response": response}


@router.post("/chart")
async def ai_chart(
    request: ChartRequest, current_user: User = Depends(get_current_user)
):
    """Generate Chart.js configuration using Gemini"""
    config = await generate_chart_config(request.description, request.data_summary)
    return config


@router.post("/ollama/chat")
async def ollama_chat(
    request: OllamaChatRequest,
    # current_user: User = Depends(get_current_user)
):
    """
    Chat using local Ollama model with streaming support.

    - Uses qwen2.5:0.5b by default (389MB, very fast)
    - Temperature: 0-1 (higher = more creative)
    - Top-p: 0-1 (lower = more focused)
    - Stream: return streaming response if True
    """
    try:
        if request.stream:
            # Return streaming response
            async def generate():
                try:
                    async for token in chat_stream_ollama(
                        request.prompt,
                        request.model,
                        request.temperature,
                        request.top_p,
                    ):
                        yield json.dumps({"token": token}) + "\n"
                except OllamaError as e:
                    yield json.dumps({"error": str(e)}) + "\n"

            return StreamingResponse(generate(), media_type="application/x-ndjson")
        else:
            # Return full response
            response = await chat_with_ollama(
                request.prompt, request.model, request.temperature, request.top_p
            )
            return {"response": response}

    except OllamaError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in Ollama chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/ollama/answer")
async def ollama_answer_question(
    prompt: str = Body(..., embed=True),
    context: str = Body("", embed=True),
    current_user: User = Depends(get_current_user),
):
    """
    Answer a question using Ollama, optionally with provided context.

    Useful for Q&A over documents or data.
    """
    try:
        response = await answer_question(prompt, context)
        return {"response": response}
    except OllamaError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.post("/ollama/summarize")
async def ollama_summarize(
    request: SummaryRequest, current_user: User = Depends(get_current_user)
):
    """
    Generate a summary of provided text using Ollama.

    - Concise summaries in specified max_length (words)
    - Good for extracting key points from documents
    """
    try:
        summary = await generate_summary(request.text, request.max_length)
        return {"summary": summary}
    except OllamaError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/ollama/health")
async def ollama_health():
    """Check if Ollama service is running and healthy"""
    is_healthy = await check_ollama_health()
    return {
        "status": "healthy" if is_healthy else "unavailable",
        "healthy": is_healthy,
    }


@router.get("/ollama/models")
async def ollama_models(current_user: User = Depends(get_current_user)):
    """
    Get list of available models in Ollama.

    Returns model names that can be used in chat endpoint.
    """
    try:
        models = await list_available_models()
        return {"models": models}
    except OllamaError as e:
        raise HTTPException(status_code=503, detail=str(e))

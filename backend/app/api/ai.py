from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from app.ai.graph import graph
from app.tts.kokoro_service import tts

router = APIRouter(prefix="/ai", tags=["AI"])


class ChatRequest(BaseModel):
    session_id: str
    message: str


@router.post("/chat")
async def chat(request: ChatRequest):

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(content=request.message)
            ]
        },
        config={
            "configurable": {
                "thread_id": request.session_id
            }
        },
    )

    response_text = ""
    for msg in reversed(result["messages"]):
        content = getattr(msg, "content", None)
        if content:
            response_text = content
            break

    audio_file = tts.generate_audio(response_text)

    return {
        "response": response_text,
        "audio": f"http://127.0.0.1:8001/audio/{audio_file}",
    }
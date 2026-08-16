from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.voice.session import VoiceSession

router = APIRouter()


@router.websocket("/voice")
async def voice(websocket: WebSocket):

    await websocket.accept()

    print("🎤 Client Connected")

    session = VoiceSession(websocket)

    try:

        await session.start()

    except WebSocketDisconnect:

        print("Client disconnected")
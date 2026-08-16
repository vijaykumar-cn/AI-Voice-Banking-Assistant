import asyncio
import json
import re
from fastapi import WebSocketDisconnect
from langchain_core.messages import HumanMessage
from app.ai.graph import graph
from app.ai.tools.customer_tool import verify_customer
from app.tts.kokoro_service import tts
from app.voice.audio_queue import audio_queue
from app.voice.pipeline import VoicePipeline
from app.voice.transcript_queue import transcript_queue
from app.voice.session_state import SessionState

def normalize_transcript_text(text: str) -> str:
    """
    Normalize transcripts.
    Examples: C U S T 1 0 0 1 -> cust1001
              C U S T one zero zero one -> cust1001
    """
    if not text:
        return text
    
    s = text.lower()
    
    # Convert spoken digits into numbers
    digit_words = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    for word, digit in digit_words.items():
        s = re.sub(rf"\b{word}\b", digit, s)
        
    def collapse(match):
        chars = re.findall(r"[a-z0-9]", match.group(0))
        return "".join(chars)
        
    s = re.sub(
        r"(?:(?:\b[a-z0-9]\b)\s+){1,}(?:\b[a-z0-9]\b)", 
        collapse, 
        s,
    )
    return s

class VoiceSession:
    def __init__(self, websocket):
        self.websocket = websocket
        self.pipeline = None
        self.state = SessionState()
        self.transcript_task = None

    async def _dg_status(self, status: str):
        try:
            await self.websocket.send_json({"dg_status": status})
        except Exception:
            pass

    async def start(self):
        self.pipeline = VoicePipeline(status_callback=self._dg_status)
        await self.pipeline.start()
        self.transcript_task = asyncio.create_task(self.process_transcripts())
        
        try:
            while True:
                try:
                    message = await self.websocket.receive()
                except RuntimeError:
                    print("⚠️ WebSocket already disconnected")
                    break
                    
                # Browser disconnected
                if message["type"] == "websocket.disconnect":
                    print("🔌 Browser disconnected")
                    break
                    
                # Audio data
                if message.get("bytes"):
                    await audio_queue.put(message["bytes"])
                    continue
                    
                # Text data
                if message.get("text"):
                    try:
                        data = json.loads(message["text"])
                    except Exception:
                        data = None
                        
                    if isinstance(data, dict):
                        if data.get("type") == "utterance_end":
                            print("✅ Received utterance_end from frontend")
                            try:
                                await self.pipeline.dg.send_finalize()
                            except Exception as e:
                                print("Finalize Error:", e)
                                
        except WebSocketDisconnect:
            print("Client disconnected")
        finally:
            print("🛑 Stopping Voice Pipeline...")
            if self.transcript_task:
                self.transcript_task.cancel()
                try:
                    await self.transcript_task
                except asyncio.CancelledError:
                    pass
            if self.pipeline:
                try:
                    await self.pipeline.stop()
                except Exception as e:
                    print("Pipeline Stop Error:", e)
            print("✅ Voice Pipeline stopped")

    async def process_transcripts(self):
        try:
            while True:
                transcript = await transcript_queue.get()
                print(f"\n🎤 {transcript}\n")
                
                normalized = normalize_transcript_text(transcript)
                print("Normalized:", normalized)
                print("Raw Transcript:", transcript)

                # -------------------------------------------------
                # Detect Customer ID
                # -------------------------------------------------
                customer_id = None
                # Extract any 4-10 digit number from the transcript
                match = re.search(r"(\d{4,10})", normalized)
                if match:
                    customer_id = f"CUST{match.group(1)}"
                    print("Detected Customer ID:", customer_id)
                    
                    result = verify_customer.invoke({"customer_id": customer_id})
                    if not result["authenticated"]:
                        await self.websocket.send_json({
                            "text": "Customer ID not found. Please try again.",
                            "audio": None,
                        })
                        continue
                    self.state.customer_db_id = result["id"]     
                    self.state.customer_id = result["customer_id"]
                    self.state.customer_name = result["customer_name"]
                    self.state.verified = True
                    
                    welcome = (
                        f"Welcome {self.state.customer_name}. "
                        f"Your identity has been verified. "
                        f"How can I help you today?"
                    )
                    print("\n🤖", welcome)
                    audio_file = tts.generate_audio(welcome)
                    await self.websocket.send_json({
                        "text": welcome,
                        "audio": f"http://127.0.0.1:8001/audio/{audio_file}",
                        "customer": {
                            "id": self.state.customer_db_id,
                            "customer_id": self.state.customer_id,
                            "name": self.state.customer_name,
                  },
                    })
                    continue
                    
                # -------------------------------------------------
                # Build Prompt
                # -------------------------------------------------
                message = normalized or transcript
                if self.state.verified:
                    message = f"""
                    Database Customer ID: {self.state.customer_db_id}
                    Customer ID: {self.state.customer_id}
                    Customer Name: {self.state.customer_name}

                    IMPORTANT:
                    When calling get_customer_loan, ALWAYS use the Database Customer ID.

                    User Request: {message}
                    """
                    
                result = graph.invoke(
                    {"messages": [HumanMessage(content=message)]},
                    config={"configurable": {"thread_id": "voice-session"}},
                )
                
                answer = ""
                for msg in reversed(result["messages"]):
                    content = getattr(msg, "content", None)
                    if content:
                        answer = content
                        break

                print(f"\n🤖 {answer}\n")
                
                audio_file = tts.generate_audio(answer)

                # Build response payload. Use the actual model answer as the text
                # and only include customer info when the session has a verified
                # customer to avoid referencing an undefined 'welcome' variable.
                payload = {
                    "text": answer,
                    "audio": f"http://127.0.0.1:8001/audio/{audio_file}",
                }
                if self.state.verified:
                    payload["customer"] = {
                        "id": self.state.customer_id,
                        "name": self.state.customer_name,
                    }

                await self.websocket.send_json(payload)
                
        except asyncio.CancelledError:
            return

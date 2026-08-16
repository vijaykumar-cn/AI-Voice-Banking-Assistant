import asyncio
import json
import websockets

from app.config.settings import settings
from app.voice.transcript_queue import transcript_queue


class DeepgramWS:

    def __init__(self, status_callback=None):
        self.ws = None
        self.keepalive_task = None
        self.status_callback = status_callback
        self._reconnect_lock = asyncio.Lock()

    async def _call_status(self, status):

        if not self.status_callback:
            return

        try:
            result = self.status_callback(status)

            if asyncio.iscoroutine(result):
                await result

        except Exception as e:
            print("Status callback:", e)

    async def connect(self):

        if self.keepalive_task:

            self.keepalive_task.cancel()

            try:
                await self.keepalive_task
            except asyncio.CancelledError:
                pass

            self.keepalive_task = None

        url = (
            "wss://api.deepgram.com/v1/listen"
            "?model=nova-3"
            "&encoding=linear16"
            "&sample_rate=16000"
            "&channels=1"
            "&language=en-US"
            "&smart_format=true"
        )

        self.ws = await websockets.connect(
            url,
            additional_headers={
                "Authorization": f"Token {settings.DEEPGRAM_API_KEY}"
            },
            max_size=None,
        )

        print("✅ Connected to Deepgram")

        await self._call_status("connected")

        self.keepalive_task = asyncio.create_task(
            self.keepalive_loop()
        )

    async def reconnect(self):

        async with self._reconnect_lock:

            if self.ws:
                return

            delay = 1

            while True:

                try:

                    print("Reconnecting Deepgram...")

                    await self.connect()

                    await self._call_status("reconnected")

                    print("✅ Reconnected")

                    return

                except Exception as e:

                    print("Reconnect failed:", e)

                    await asyncio.sleep(delay)

                    delay = min(delay * 2, 10)

    async def keepalive_loop(self):

        try:

            while True:

                await asyncio.sleep(10)

                if not self.ws:
                    break

                try:

                    await self.ws.send(
                        json.dumps(
                            {
                                "type": "KeepAlive"
                            }
                        )
                    )

                except Exception:

                    self.ws = None

                    await self._call_status("disconnected")

                    break

        except asyncio.CancelledError:
            return

    async def send_finalize(self):

        if not self.ws:
            return

        try:

            print("📤 Sending Finalize")

            await self.ws.send(
                json.dumps(
                    {
                        "type": "Finalize"
                    }
                )
            )

        except Exception as e:

            print("Finalize error:", e)

    async def send_audio(self, audio):

        if not self.ws:
            await self.reconnect()

        if not self.ws:
            return

        try:

            print(f"Sending PCM: {len(audio)} bytes")
            await self.ws.send(audio)

        except websockets.ConnectionClosed:

            print("Deepgram socket closed")

            self.ws = None

            await self._call_status("disconnected")

        except Exception as e:

            print("send_audio:", e)

            self.ws = None

    async def receive_loop(self):

        while True:

            if not self.ws:

                await self.reconnect()

                if not self.ws:
                    await asyncio.sleep(1)
                    continue

            try:

                message = await self.ws.recv()

                try:
                    data = json.loads(message)

                except Exception as e:

                    print("JSON Parse Error:", e)

                    continue

                if data.get("type") != "Results":
                    continue

                print("\n========== DEEPGRAM RESULT ==========")
                print(json.dumps(data, indent=2))
                print("=====================================\n")

                channel = data.get("channel", {})
                alternatives = channel.get("alternatives", [])

                if not alternatives:

                    print("❌ No alternatives found")

                    continue

                transcript = alternatives[0].get(
                    "transcript",
                    ""
                ).strip()

                is_final = data.get(
                    "is_final",
                    False
                )

                speech_final = data.get(
                    "speech_final",
                    False
                )

                print(
                    f"is_final={is_final} | speech_final={speech_final}"
                )

                if transcript:

                    if is_final:

                        print("🎤 FINAL:", transcript)

                    else:

                        print("🎤 PARTIAL:", transcript)

                    # Only send FINAL transcript to LangGraph
                    if is_final:

                        await transcript_queue.put(
                            transcript
                        )

            except websockets.ConnectionClosed as e:

                if e.code == 1011:

                    print("Deepgram idle timeout")

                else:

                    print("Deepgram closed:", e)

                self.ws = None

                await self._call_status(
                    "disconnected"
                )

                if self.keepalive_task:

                    self.keepalive_task.cancel()

                    self.keepalive_task = None

                await asyncio.sleep(1)

            except asyncio.CancelledError:

                break

            except Exception as e:

                print("receive_loop:", e)

                self.ws = None

                await self._call_status(
                    "disconnected"
                )

                await asyncio.sleep(1)

    async def close(self):

        if self.keepalive_task:

            self.keepalive_task.cancel()

            try:
                await self.keepalive_task

            except asyncio.CancelledError:
                pass

            self.keepalive_task = None

        if self.ws:

            try:

                await self.ws.close()

            except Exception:
                pass

            self.ws = None

        await self._call_status("disconnected")

        print("✅ Deepgram closed")

import asyncio
import time

from app.voice.audio_queue import audio_queue
from app.voice.deepgram_ws import DeepgramWS


class VoicePipeline:

    def __init__(self, status_callback=None):

        self.dg = DeepgramWS(
            status_callback=status_callback
        )

        self.receive_task = None
        self.send_task = None

    async def start(self):

        await self.dg.connect()

        self.receive_task = asyncio.create_task(
            self.dg.receive_loop()
        )

        self.send_task = asyncio.create_task(
            self.send_loop()
        )

    async def send_loop(self):

        try:

            while True:

                audio = await audio_queue.get()

                try:
                    print(
                        f"Pipeline: dequeued {len(audio)} bytes @ {time.time()}"
                    )
                except Exception:
                    pass

                try:

                    await self.dg.send_audio(audio)

                except asyncio.CancelledError:
                    raise

                except Exception as e:

                    print("Pipeline send error:", e)

                    break

        except asyncio.CancelledError:

            print("Pipeline send loop cancelled")

        finally:

            print("Pipeline send loop stopped")

    async def stop(self):

        print("Stopping Voice Pipeline...")

        # Ask Deepgram to finalize transcription
        try:

            await self.dg.send_finalize()

            await asyncio.sleep(0.7)

        except Exception:
            pass

        # Cancel background tasks
        for task in [self.send_task, self.receive_task]:

            if task and not task.done():

                task.cancel()

        # Wait for them to exit cleanly
        await asyncio.gather(
            *(t for t in [self.send_task, self.receive_task] if t),
            return_exceptions=True,
        )

        # Close Deepgram websocket
        try:

            await self.dg.close()

        except Exception:
            pass

        print("Voice Pipeline stopped")
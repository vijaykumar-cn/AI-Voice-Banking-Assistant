import asyncio

from app.voice.deepgram_ws import DeepgramWS


async def main():

    dg = DeepgramWS()

    await dg.connect()

    print("Connected!")


asyncio.run(main())
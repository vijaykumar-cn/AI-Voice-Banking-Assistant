from deepgram import DeepgramClient

from app.config.settings import settings


class DeepgramService:
    def __init__(self):
        self.client = DeepgramClient(settings.DEEPGRAM_API_KEY)


deepgram_service = DeepgramService()
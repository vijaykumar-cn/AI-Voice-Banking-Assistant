from typing import TypedDict
from langchain_core.messages import BaseMessage


class BankingState(TypedDict):
    messages: list[BaseMessage]
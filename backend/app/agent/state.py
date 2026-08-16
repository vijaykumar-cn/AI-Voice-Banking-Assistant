from typing import TypedDict


class BankingState(TypedDict):
    user_input: str
    customer_id: str | None
    authenticated: bool
    intent: str | None
    tool_result: dict | None
    response: str
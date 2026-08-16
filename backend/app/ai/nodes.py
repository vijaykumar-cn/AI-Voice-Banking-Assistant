from langchain_core.messages import HumanMessage, SystemMessage

from app.ai.llm import get_llm
from app.ai.prompts import SYSTEM_PROMPT


def chatbot_node(state):
    llm = get_llm()

    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["user_input"]),
        ]
    )

    return {
        "response": response.content
    }
from langgraph.prebuilt import create_react_agent

from app.ai.llm import get_llm
from app.ai.prompts import SYSTEM_PROMPT
from app.ai.tools.customer_tool import verify_customer
from app.ai.tools.loan_tool import get_customer_loan, get_loan_types


banking_agent = create_react_agent(
    model=get_llm(),
    tools=[
        verify_customer,
        get_customer_loan,
        get_loan_types,
    ],
    prompt=SYSTEM_PROMPT,
)
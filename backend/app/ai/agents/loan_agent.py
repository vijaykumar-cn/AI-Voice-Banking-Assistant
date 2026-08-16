from langgraph.prebuilt import create_react_agent

from app.ai.llm import get_llm
from app.ai.tools.loan_tool import get_customer_loan, get_loan_types


loan_agent = create_react_agent(
    model=get_llm(),
    tools=[get_customer_loan, get_loan_types],
)
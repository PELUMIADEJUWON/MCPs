from dotenv import load_dotenv
import os, json, requests

load_dotenv(override=True)
key = os.getenv("API_TOKEN")
print("KEY:", key[:12] if key else "NOT FOUND", "| length:", len(key) if key else 0)

os.environ["OPENROUTER_API_KEY"] = key

from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool

llm = LLM(
    model="openrouter/openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("API_TOKEN")
)

@tool("convert_currency")
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another."""
    r = requests.post(
        "http://127.0.0.1:8000/mcp",
        headers={"Accept": "application/json, text/event-stream",
                 "Content-Type": "application/json"},
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "convert_currency",
                         "arguments": {"amount": amount,
                                       "from_currency": from_currency,
                                       "to_currency": to_currency}}}
    )
    return r.text

currency_agent = Agent(
    role="Currency Converter",
    goal="Help users convert currencies using the conversion tool",
    backstory="You always use the convert_currency tool and never guess rates.",
    tools=[convert_currency],
    llm=llm,
    verbose=True
)

conversion_task = Task(
    description="Convert 100 USD to NGN using the convert_currency tool.",
    expected_output="A clear currency conversion result.",
    agent=currency_agent
)

crew = Crew(agents=[currency_agent], tasks=[conversion_task], verbose=True)

result = crew.kickoff()
print("\nFINAL RESULT:")
print(result)
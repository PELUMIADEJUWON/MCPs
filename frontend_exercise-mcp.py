from dotenv import load_dotenv
import os
import requests
import streamlit as st

load_dotenv(override=True)

key = os.getenv("API_TOKEN")
if not key:                                    
    st.error("API_TOKEN is missing from .env")
    st.stop()

os.environ["OPENROUTER_API_KEY"] = key

from crewai import Agent, Task, Crew, LLM
from crewai.tools import tool




llm = LLM(
    model="openrouter/openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=key
)



@tool("convert_currency")
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str
) -> str:
    """Convert an amount from one currency to another using the MCP server."""

    try:                                       
        r = requests.post(
            "http://127.0.0.1:8000/mcp",
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json"
            },
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "convert_currency",
                    "arguments": {
                        "amount": amount,
                        "from_currency": from_currency,
                        "to_currency": to_currency
                    }
                }
            },
            timeout=15,
        )
        r.raise_for_status()
    except requests.RequestException as e:
        return f"Could not reach the currency server: {e}"

    data = r.json()

    if "error" in data:
        return f"MCP error: {data['error']['message']}"

    return data["result"]["content"][0]["text"]



currency_agent = Agent(
    role="Currency Converter",
    goal="Help users convert currencies using the conversion tool",
    backstory="You always use the convert_currency tool and never guess rates.",
    tools=[convert_currency],
    llm=llm,
    max_iter=3,
    verbose=True
)


# =========================
# STREAMLIT FRONTEND
# =========================

st.title("💱 Currency Converter")

st.write("Convert currencies using CrewAI and MCP.")


amount = st.number_input(
    "Enter amount",
    min_value=0.01,
    value=100.00
)


from_currency = st.selectbox(
    "From",
    ["USD", "GBP", "EUR", "NGN"]
)


to_currency = st.selectbox(
    "To",
    ["USD", "GBP", "EUR", "NGN"]
)


if st.button("Convert"):
    if from_currency == to_currency:           
        st.warning("Pick two different currencies.")
        st.stop()
    conversion_task = Task(
        description=f"""
        Convert {amount} {from_currency} to {to_currency}
        using the convert_currency tool.

        Do not guess the exchange rate.
        Use the tool to get the conversion result.
        """,
        expected_output="A clear currency conversion result.",
        agent=currency_agent
    )

    crew = Crew(
        agents=[currency_agent],
        tasks=[conversion_task],
        verbose=True
    )

    with st.spinner("Converting..."):
        result = crew.kickoff()

    st.success(result.raw)
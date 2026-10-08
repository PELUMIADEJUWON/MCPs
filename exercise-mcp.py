from mcp.server import MCPServer

mcp = MCPServer("Currency Converter")


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert an amount from one currency to another."""

    rates = {
        "USD_NGN": 1500,
        "GBP_NGN": 2000,
        "EUR_NGN": 1700,
        "USD_GBP": 0.75,
        "USD_EUR": 0.85,
    }

    pair = f"{from_currency.upper()}_{to_currency.upper()}"

    if pair not in rates:
        return "Sorry, I don't have that currency conversion yet."

    result = amount * rates[pair]

    return f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}"



@mcp.resource("currency://supported")
def supported_currencies() -> str:
    """List supported currencies."""

    return """
Supported currencies:

USD - US Dollar
GBP - British Pound
EUR - Euro
NGN - Nigerian Naira
"""


@mcp.prompt()
def convert_money(amount: str, from_currency: str, to_currency: str) -> str:
    """Create a currency conversion prompt."""

    return f"Convert {amount} {from_currency} to {to_currency}."


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        stateless_http=True,
        json_response=True,
    )

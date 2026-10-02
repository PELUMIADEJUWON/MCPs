from fastmcp import FastMCP

mcp = FastMCP("My First Server")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.resource("docs://mcp/concepts")
def mcp_docs() -> str:
    """Documentation about MCP concepts."""
    return """MCP has three primitives:
1. Tools — functions the LLM can call
2. Resources — read-only data the app loads
3. Prompts — reusable templates the user invokes"""


@mcp.prompt()
def code_review(code: str, language: str) -> str:
    """Generate a code review prompt."""
    return f"""Please review this {language} code for bugs, style, and performance:

{code}"""


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
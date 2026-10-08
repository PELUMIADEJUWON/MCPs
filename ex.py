import requests
r = requests.post(
    "http://127.0.0.1:8000/mcp",
    headers={"Accept": "application/json, text/event-stream",
             "Content-Type": "application/json"},
    json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "convert_currency",
                     "arguments": {"amount": 100, "from_currency": "USD", "to_currency": "NGN"}}}
)
print(r.status_code)
print(r.text)
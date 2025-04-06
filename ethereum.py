import os
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("ethereum")

ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")
if not ALCHEMY_API_KEY:
    raise ValueError("ALCHEMY_API_KEY environment variable is not set")

ALCHEMY_API_URL = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

async def make_alchemy_request(url: str, payload: dict[str, Any]) -> dict[str, Any] | None:
    """Make a request to the Alchemy API with proper error handling."""
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def _hex_to_int(hex_str: str) -> int:
    return int(hex_str, 16)
        
@mcp.tool()
async def get_transaction_receipt(tx_hash: str) -> str:
    """Get the transaction details for a given transaction hash."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionReceipt",
        "params": [tx_hash],
        "id": 1
    }
    transaction_receipt = await make_alchemy_request(ALCHEMY_API_URL, payload)
    
    return f"""
    From: {transaction_receipt["result"]["from"]}
    To: {transaction_receipt["result"]["to"]}
    Gas used: {_hex_to_int(transaction_receipt["result"]["gasUsed"])}
    """

if __name__ == "__main__":
    mcp.run(transport='stdio')

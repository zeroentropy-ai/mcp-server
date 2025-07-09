from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy
from dotenv import load_dotenv
from os import getenv
import sys

from tools.collections import register_collection_tools
from tools.documents import register_document_tools
from tools.queries import register_query_tools
from tools.models import register_model_tools
from tools.status import register_status_tools

load_dotenv()

mcp = FastMCP("zeroentropy")

# Check if running in development mode
api_key = getenv("ZEROENTROPY_API_KEY")
if not api_key:
    if len(sys.argv) > 1 and sys.argv[1] == "--dev":
        print("Running in development mode without API key")
        zeroentropy_client = None
    else:
        print("Error: ZEROENTROPY_API_KEY environment variable is required", file=sys.stderr)
        print("For development, use: uv run server.py --dev", file=sys.stderr)
        sys.exit(1)
else:
    zeroentropy_client = ZeroEntropy(api_key=api_key)

register_collection_tools(mcp, zeroentropy_client)
register_document_tools(mcp, zeroentropy_client)
register_query_tools(mcp, zeroentropy_client)
register_model_tools(mcp, zeroentropy_client)
register_status_tools(mcp, zeroentropy_client)

if __name__ == "__main__":
    mcp.run(transport="stdio")

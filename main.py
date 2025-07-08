from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy
from dotenv import load_dotenv
from os import getenv
load_dotenv()

mcp = FastMCP("zeroentropy")

zeroentropy_client = ZeroEntropy(
    api_key=getenv("ZEROENTROPY_API_KEY")
)

@mcp.tool()
async def get_collection_list() -> list[str]:
    response = zeroentropy_client.collections.get_list()
    return response.collections

if __name__ == "__main__":
    mcp.run(transport="stdio")

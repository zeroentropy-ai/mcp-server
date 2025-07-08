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
    return response.collection_names

@mcp.tool()
async def add_collection(collection_name: str) -> None:
    zeroentropy_client.collections.add(collection_name=collection_name)

@mcp.tool()
async def delete_collection(collection_name: str) -> None:
    zeroentropy_client.collections.delete(collection_name=collection_name)

@mcp.tool()
async def add_document(collection_name: str, path: str, content: dict) -> None:
    zeroentropy_client.documents.add(collection_name=collection_name, path=path, content=content)

@mcp.tool()
async def get_document_info(collection_name: str, path: str, include_content: bool = False) -> dict:
    zeroentropy_client.documents.get_info(collection_name=collection_name, path=path, include_content=include_content)

@mcp.tool()
async def get_document_info_list(collection_name: str, limit: int = 100, path_prefix: str | None = None, path_gt: str | None = None) -> list[str]:
    zeroentropy_client.documents.get_info_list(
        collection_name=collection_name, limit=limit, path_prefix=path_prefix, path_gt=path_gt
    )

@mcp.tool()
async def delete_document(collection_name: str, path: str) -> None:
    zeroentropy_client.documents.delete(collection_name=collection_name, path=path)


@mcp.tool()
async def get_page_info(collection_name: str, path: str, page_index: int, include_content: bool = False) -> dict:
    zeroentropy_client.documents.get_page_info(collection_name=collection_name, path=path, page_index=page_index, include_content=include_content)

if __name__ == "__main__":
    mcp.run(transport="stdio")

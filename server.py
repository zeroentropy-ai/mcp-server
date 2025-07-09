from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy
from dotenv import load_dotenv
from os import getenv
import sys

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
    response = zeroentropy_client.documents.get_info(collection_name=collection_name, path=path, include_content=include_content)
    return response.document.model_dump()

@mcp.tool()
async def get_document_info_list(collection_name: str, limit: int = 1024, path_prefix: str | None = None, path_gt: str | None = None) -> list[dict]:
    response = zeroentropy_client.documents.get_info_list(
        collection_name=collection_name, limit=limit, path_prefix=path_prefix, path_gt=path_gt
    )
    
    return [doc.model_dump() for doc in response.documents]

@mcp.tool()
async def delete_document(collection_name: str, path: str) -> None:
    zeroentropy_client.documents.delete(collection_name=collection_name, path=path)


@mcp.tool()
async def get_page_info(collection_name: str, path: str, page_index: int, include_content: bool = False) -> dict:
    response = zeroentropy_client.documents.get_page_info(collection_name=collection_name, path=path, page_index=page_index, include_content=include_content)
    return response.page.model_dump()

@mcp.tool()
async def get_top_documents(collection_name: str, query: str, k: int, filter: dict | None = None, include_metadata: bool = False, reranker: str | None = None) -> list[dict]:
    response = zeroentropy_client.queries.top_documents(
        collection_name=collection_name, 
        query=query, 
        k=k, 
        filter=filter, 
        include_metadata=include_metadata, 
        reranker=reranker
    )
    return [result.model_dump() for result in response.results]

@mcp.tool()
async def get_top_pages(collection_name: str, query: str, k: int, filter: dict | None = None, include_content: bool = False, latency_mode: str | None = "low") -> list[dict]:
    response = zeroentropy_client.queries.top_pages(
        collection_name=collection_name, 
        query=query, 
        k=k, 
        filter=filter, 
        include_content=include_content,
        latency_mode=latency_mode
    )
    return [result.model_dump() for result in response.results]

@mcp.tool()
async def get_top_snippets(collection_name: str, query: str, k: int, reranker: str | None = None, filter: dict | None = None, 
                            precise_responses: bool = False, include_document_metadata: bool = False) -> list[dict]:
    response = zeroentropy_client.queries.top_snippets(
        collection_name=collection_name, 
        query=query, 
        k=k, 
        reranker=reranker,
        filter=filter, 
        precise_responses=precise_responses,
        include_document_metadata=include_document_metadata,
    )
    return [result.model_dump() for result in response.results]

if __name__ == "__main__":
    mcp.run(transport="stdio")

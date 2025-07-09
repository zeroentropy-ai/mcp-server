from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy

def register_query_tools(mcp: FastMCP, zeroentropy_client: ZeroEntropy):
    """Register query-related tools with the MCP server."""

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

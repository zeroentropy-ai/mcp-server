from enum import Enum
from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy

class LatencyMode(str, Enum):
    """Latency mode options for queries."""
    LOW = "low"
    HIGH = "high"

def register_query_tools(mcp: FastMCP, zeroentropy_client: ZeroEntropy):
    """Register query-related tools with the MCP server."""

    @mcp.tool()
    async def get_top_documents(collection_name: str, query: str, k: int, filter: dict[str, str | list[str]] | None = None, include_metadata: bool = False, reranker: str | None = None, latency_mode: LatencyMode | None = LatencyMode.LOW) -> list[dict]:
        """
        Get the top K documents that match the given query using semantic search.
        
        This method searches through a collection of documents using natural language queries
        and returns the most relevant documents based on semantic similarity.
        
        Args:
            collection_name (str): The name of the collection to search in.
            query (str): The natural language query to search with. Cannot exceed 4096 UTF-8 bytes.
            k (int): The number of documents to return. Must be between 1 and 2048, inclusive.
                If there are not enough documents matching your filters, fewer may be returned.
            filter (dict[str, str | list[str]] | None, optional): Query filter to apply based on 
                document metadata. Supports operators like $eq, $ne, $gt, $gte, $lt, $lte for 
                string attributes, and $in, $nin for list attributes (prefixed with 'list:'). 
                Boolean operators $and, $or can be used to combine filters. Defaults to None 
                (searches all documents).
            include_metadata (bool, optional): Whether to include document metadata in the 
                response. Defaults to False.
            reranker (str | None, optional): The reranker model to use after initial retrieval
                for improved result quality. Use None for no reranking (default). Available 
                model IDs can be found at /models/rerank endpoint.
            latency_mode (LatencyMode | None, optional): The latency mode to use for the query.        
        Returns:
            list[dict]: A list of dictionaries containing the top matching documents. Each
                dictionary contains the document content and optionally metadata if 
                include_metadata=True.
        
        Notes:
            - Document metadata must be of type dict[str, str | list[str]]
            - List attributes in metadata must be prefixed with 'list:' (e.g., 'list:tags')
            - If a document doesn't contain a filtered attribute, it's considered null
            - For filtering examples and detailed metadata specification, see the ZeroEntropy
              documentation on Metadata Filtering
        
        Example:
            >>> # Basic search with low latency (default)
            >>> results = await get_top_documents(
            ...     collection_name="my_docs",
            ...     query="machine learning algorithms",
            ...     k=5
            ... )
            
            >>> # Search with high latency for better accuracy
            >>> results = await get_top_documents(
            ...     collection_name="my_docs", 
            ...     query="recent developments",
            ...     k=10,
            ...     latency_mode=LatencyMode.HIGH
            ... )
        """
        response = zeroentropy_client.queries.top_documents(
            collection_name=collection_name, 
            query=query, 
            k=k, 
            filter=filter, 
            include_metadata=include_metadata, 
            reranker=reranker,
            latency_mode=latency_mode.value if latency_mode else None
        )
        return [result.model_dump() for result in response.results]

    @mcp.tool()
    async def get_top_pages(collection_name: str, query: str, k: int, filter: dict | None = None, include_content: bool = False, latency_mode: LatencyMode | None = LatencyMode.LOW) -> list[dict]:
        """
        Get the top K pages that match the given query using semantic search.
        
        Args:
            collection_name (str): The name of the collection to search in.
            query (str): The natural language query to search with. Cannot exceed 4096 UTF-8 bytes.
            k (int): The number of pages to return. Must be between 1 and 2048, inclusive.
                If there are not enough pages matching your filters, fewer may be returned.
            filter (dict | None, optional): Query filter to apply based on document metadata.
                Supports the same filtering syntax as get_top_documents. Defaults to None.
            include_content (bool, optional): Whether to include the full content of the pages
                in the response. Defaults to False.
            latency_mode (LatencyMode | None, optional): The latency mode to use for the query.
        
        Returns:
            list[dict]: A list of dictionaries containing the top matching pages.
                Each object contains path, page_index, score, content and image_url.
        """
        response = zeroentropy_client.queries.top_pages(
            collection_name=collection_name, 
            query=query, 
            k=k, 
            filter=filter, 
            include_content=include_content,
            latency_mode=latency_mode.value if latency_mode else None
        )
        return [result.model_dump() for result in response.results]

    @mcp.tool()
    async def get_top_snippets(collection_name: str, query: str, k: int, reranker: str | None = None, filter: dict | None = None, 
                                precise_responses: bool = False, include_document_metadata: bool = False) -> list[dict]:
        """
        Get the top K snippets that match the given query

            collection_name (str): The name of the collection to get the top snippets from.
            query (str): The query to get the top snippets for.
            k (int): The number of top snippets to return.
            reranker (str | None): The reranker to use for reranking the snippets.
            filter (dict | None): A filter to apply to the query.
            precise_responses (bool): Whether to include the precise responses.
                If true, the responses will average 200 characters. If false, the responses will average 2000 characters.
            include_document_metadata (bool): Whether to include the metadata of the documents.
        Returns:
            list[dict]: A list of dictionaries containing the top snippets.
            Each object contains path, start_index, end_index, page_span, content, and score.
        """
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

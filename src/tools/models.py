from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy

def register_model_tools(mcp: FastMCP, zeroentropy_client: ZeroEntropy):
    """Register model-related tools with the MCP server."""

    @mcp.tool()
    async def rerank_documents(query: str, documents: list[dict], model: str = "zerank-1", top_n: int | None = None) -> list[dict]:
        """
        Reranks the provided documents, according to the provided query.

        Args:
            query (str): The query to rerank the documents by
            documents (list[dict]): The documents to rerank
            model (str): The model to use for reranking. Defaults to "zerank-1".
            top_n (int | None): The number of documents to return. Defaults to None.
        """
        response = zeroentropy_client.models.rerank(query=query, documents=documents, model=model, top_n=top_n)
        return [result.model_dump() for result in response.results]

from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy

def register_status_tools(mcp: FastMCP, zeroentropy_client: ZeroEntropy):

    @mcp.tool()
    async def get_indexing_status(collection_name: str | None = None) -> dict:
        """
        Gets the current indexing status across all documents.
        Args:
            collection_name (str | None): The name of the collection to get the indexing status for.
                If not provided, it will show the cumulative status across all of your collections.
        Returns:
            dict: A dictionary with the indexing status of the ZeroEntropy instance
        """
        response = zeroentropy_client.status.get_status(collection_name=collection_name)
        return response.model_dump()

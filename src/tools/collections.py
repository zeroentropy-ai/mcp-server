from zeroentropy import ZeroEntropy
from mcp.server.fastmcp import FastMCP

def register_collection_tools(mcp: FastMCP, zeroentropy_client: ZeroEntropy):
    """Register collection-related tools with the MCP server."""

    @mcp.tool()
    async def get_collection_list() -> list[str]:
        """
        Get a complete list of all collections
        Returns:
            list[str]: A list of collection names
            Example:
            ```
            [
                "collection_name_1",
                "collection_name_2",
                "collection_name_3"
            ]
            ```
        Raises:
            ValidationError
        """
        response = zeroentropy_client.collections.get_list()
        return response.collection_names

    @mcp.tool()
    async def add_collection(collection_name: str) -> None:
        """
        Add a new collection
        Args:
            collection_name (str): The name of the collection to add
        Returns:
            dict: A dictionary with a success key and a message key
        Raises:
            ValidationError
            If the collection already exists, a 409 Conflict status code will be returned.
        """
        zeroentropy_client.collections.add(collection_name=collection_name)
        return {
            "success": True,
            "message": f"Collection '{collection_name}' added successfully"
        }

    @mcp.tool()
    async def delete_collection(collection_name: str) -> None:
        """
        Delete a collection
        Args:
            collection_name (str): The name of the collection to delete
        Returns:
            dict: A dictionary with a success key and a message key
        Raises:
            ValidationError
            If the collection does not exist, a 404 Not Found status code will be returned.
        """
        zeroentropy_client.collections.delete(collection_name=collection_name)
        return {
            "success": True,
            "message": f"Collection '{collection_name}' deleted successfully"
        }

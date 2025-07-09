from mcp.server.fastmcp import FastMCP
from zeroentropy import ZeroEntropy

def register_document_tools(mcp: FastMCP, zeroentropy_client: ZeroEntropy):
    """Register document-related tools with the MCP server."""

    @mcp.tool()
    async def add_document(collection_name: str, path: str, content: dict) -> None:
        """
        Add a new document to a collection.
        
        Args:
            collection_name (str): The name of the collection to add the document to. 
                A 404 Not Found status code will be returned if this collection name does not exist.
            path (str): The path of the document to add. 
                A 409 Conflict status code will be returned if this path already exists.
            content (dict): The content of the document to add. Must be one of three types:
                
                For text documents:
                {
                    "type": "text",
                    "text": "The content of this document, as a text string"
                }
                
                For paginated text documents:
                {
                    "type": "text-pages", 
                    "pages": ["Page 1 content", "Page 2 content", ...]
                }
                Note: Pages are 0-indexed, so the first page has index 0, second has index 1, etc.
                
                For binary documents:
                {
                    "type": "auto",
                    "base64_data": "base64-encoded string of the file's raw data"
                }
                Note: File extension and binary data are used to automatically deduce filetype.
        
        Returns:
            dict: A dictionary with a success key and a message key
        
        Raises:
            ValidationError: If the content structure is invalid
            404: If the collection doesn't exist
            409: If the document path already exists
        
        Examples:
            # Add a text document
            await add_document("my_collection", "doc1.txt", {
                "type": "text",
                "text": "Hello, world!"
            })
            
            # Add a paginated document
            await add_document("my_collection", "doc2.txt", {
                "type": "text-pages",
                "pages": ["First page content", "Second page content"]
            })
            
            # Add a binary document
            await add_document("my_collection", "image.png", {
                "type": "auto",
                "base64_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
            })
        """
        zeroentropy_client.documents.add(collection_name=collection_name, path=path, content=content)
        return {
            "success": True,
            "message": f"Document '{path}' added to collection '{collection_name}'"
        }

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
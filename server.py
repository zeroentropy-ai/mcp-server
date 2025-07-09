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

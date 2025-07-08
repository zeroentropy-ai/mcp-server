from pydantic import BaseModel
from datetime import datetime

class DocumentInfo(BaseModel):
    id: str
    collection_name: str
    path: str
    metadata: dict
    index_status: str
    created_at: datetime
    size: int
    num_pages: int
    file_url: str

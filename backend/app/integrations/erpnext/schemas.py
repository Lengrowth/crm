from pydantic import BaseModel
from typing import Optional


class ERPNextOperationResult(BaseModel):
    status: str
    site_name: Optional[str] = None
    mock: bool = True
    action: Optional[str] = None

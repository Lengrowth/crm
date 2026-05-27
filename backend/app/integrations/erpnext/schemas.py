from pydantic import BaseModel


class ERPNextOperationResult(BaseModel):
    status: str
    site_name: str | None = None
    mock: bool = True
    action: str | None = None

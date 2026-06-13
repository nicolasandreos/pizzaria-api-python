from pydantic import BaseModel
from datetime import datetime, timezone

class ErrorSchema(BaseModel):
    timestamp: str = datetime.now(timezone.utc).isoformat()
    success: bool = False
    message: str
    status_code: int
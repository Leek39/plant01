from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    """
    -title : required
    -completed : optional
    """
    title: str
    completed: bool = False


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


class TodoResponse(BaseModel):
    id : int
    title : str
    completed : bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes  = True

class APIResponse(BaseModel):
    status : str
    data : Optional[dict] = None
    message : Optional[str] = None


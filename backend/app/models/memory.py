from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID, uuid4


class MemoryBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: Any = Field(...)
    ttl: Optional[datetime] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class MemoryCreate(MemoryBase):
    pass


class MemoryUpdate(BaseModel):
    key: Optional[str] = Field(None, min_length=1, max_length=100)
    value: Optional[Any] = None
    ttl: Optional[datetime] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class Memory(MemoryBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class MemoryList(BaseModel):
    memories: List[Memory]
    total: int

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    price: float = Field(..., ge=0)
    tags: List[str] = Field(default_factory=list)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    price: Optional[float] = Field(default=None, ge=0)
    tags: Optional[List[str]] = None

class ItemOut(ItemBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
from typing import Optional
from pydantic import BaseModel, Field


class SoftwareCreate(BaseModel):
    name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    website: Optional[str] = None


class SoftwareResponse(BaseModel):
    id: str
    name: str
    description: str
    website: Optional[str]
    createdAt: str

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    softwareId: str
    name: str = Field(..., min_length=1)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=1)


class ReviewResponse(BaseModel):
    id: str
    softwareId: str
    name: str
    rating: int
    comment: str
    createdAt: str

    class Config:
        from_attributes = True

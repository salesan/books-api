from typing import Optional
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, min_length=1)
    author: str = Field(max_length=100, min_length=1)
    pages: int = Field(ge=1)
    rating: float = Field(ge=0, le=5)
    price: float = Field(ge=0)

class BookCreate(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(max_length=100, min_length=1)
    author: str = Field(max_length=100, min_length=1)
    pages: int = Field(ge=1)
    rating: float = Field(ge=0, le=5)
    price: float = Field(ge=0)

class BookUpdate(SQLModel):
    rating: Optional[float] = Field(ge=0, le=5)
    price: Optional[float] = Field(ge=0)

"""
Schemas Pydantic
================
Define los modelos de datos para validación.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class SortOrder(str, Enum):
    """Orden de clasificación"""
    asc = "asc"
    desc = "desc"


class ProductSortField(str, Enum):
    """Campos para ordenar productos"""
    name = "name"
    price = "price"
    created_at = "created_at"

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    price: float = Field(..., gt=0)
    coverage_amount: float = Field(..., gt=0)


class ProductCreate(ProductBase):
    category_id: int = Field(..., gt=0)


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    coverage_amount: float | None = None
    category_id: int | None = None


class ProductResponse(ProductBase):
    id: int
    category_id: int
    created_at: datetime
    category: CategoryResponse | None = None

    model_config = {"from_attributes": True}

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool

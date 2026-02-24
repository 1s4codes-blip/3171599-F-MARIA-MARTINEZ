"""
Router de Categorías
====================

CRUD completo para categorías.
"""

from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime

from database import categories_db, get_next_category_id
from schemas import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Tipos de Seguro"]
)

@router.get("/", response_model=list[CategoryResponse])
async def list_categories():
    return list(categories_db.values())

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int = Path(..., gt=0)
):
    category = categories_db.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate):
    new_id = get_next_category_id()
    new_category = {
        "id": new_id,
        **category.model_dump(),
        "created_at": datetime.utcnow()
    }
    categories_db[new_id] = new_category
    return new_category

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int = Path(..., gt=0),
    category: CategoryCreate = ...
):
    if category_id not in categories_db:
        raise HTTPException(status_code=404, detail="Category not found")

    updated = {
        "id": category_id,
        **category.model_dump(),
        "created_at": categories_db[category_id]["created_at"]
    }

    categories_db[category_id] = updated
    return updated

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int = Path(..., gt=0)
):
    if category_id not in categories_db:
        raise HTTPException(status_code=404, detail="Category not found")

    del categories_db[category_id]
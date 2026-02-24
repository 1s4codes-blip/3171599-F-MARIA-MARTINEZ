from fastapi import APIRouter, Path, HTTPException, status
from datetime import datetime

from database import products_db, categories_db, get_next_product_id
from schemas import ProductCreate, ProductUpdate
from dependencies import PaginationDep, ProductFiltersDep, SortingDep

router = APIRouter(
    prefix="/products",
    tags=["Seguros"]
)


@router.get("/")
async def list_products(
    pagination: PaginationDep,
    filters: ProductFiltersDep,
    sorting: SortingDep
):
    products = list(products_db.values())

    # Filtros
    if filters.search:
        products = [
            p for p in products
            if filters.search.lower() in p["name"].lower()
        ]

    if filters.category_id:
        products = [
            p for p in products
            if p["category_id"] == filters.category_id
        ]

    if filters.min_price is not None:
        products = [p for p in products if p["price"] >= filters.min_price]

    if filters.max_price is not None:
        products = [p for p in products if p["price"] <= filters.max_price]

    # Ordenamiento
    reverse = sorting.order == "desc"
    products.sort(key=lambda x: x[sorting.sort_by], reverse=reverse)

    total = len(products)
    start = pagination.offset
    end = start + pagination.per_page
    paginated = products[start:end]

    return {
        "items": paginated,
        "total": total,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "pages": (total + pagination.per_page - 1) // pagination.per_page,
        "has_next": end < total,
        "has_prev": pagination.page > 1
    }


@router.get("/{product_id}")
async def get_product(
    product_id: int = Path(..., gt=0)
):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    category = categories_db.get(product["category_id"])
    product["category"] = category
    return product


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductCreate):
    if product.category_id not in categories_db:
        raise HTTPException(status_code=400, detail="Category not found")

    new_id = get_next_product_id()
    new_product = {
        "id": new_id,
        **product.model_dump(),
        "created_at": datetime.utcnow()
    }

    products_db[new_id] = new_product
    return new_product


@router.put("/{product_id}")
async def replace_product(
    product_id: int = Path(..., gt=0),
    product: ProductCreate = ...
):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.category_id not in categories_db:
        raise HTTPException(status_code=400, detail="Category not found")

    updated = {
        "id": product_id,
        **product.model_dump(),
        "created_at": products_db[product_id]["created_at"]
    }

    products_db[product_id] = updated
    return updated


@router.patch("/{product_id}")
async def update_product(
    product_id: int = Path(..., gt=0),
    product: ProductUpdate = ...
):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = products_db[product_id]

    update_data = product.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        if update_data["category_id"] not in categories_db:
            raise HTTPException(status_code=400, detail="Category not found")

    existing.update(update_data)
    products_db[product_id] = existing

    return existing


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int = Path(..., gt=0)
):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    del products_db[product_id]
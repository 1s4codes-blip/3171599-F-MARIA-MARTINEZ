"""
Define dependencias para paginación, filtros y ordenamiento.
"""

from fastapi import Query, Depends
from typing import Annotated
from schemas import SortOrder, ProductSortField

class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=50)
    ):
        self.page = page
        self.per_page = per_page
        self.offset = (page - 1) * per_page


PaginationDep = Annotated[PaginationParams, Depends()]

class ProductFilters:
    def __init__(
        self,
        search: str | None = Query(default=None, min_length=2),
        category_id: int | None = Query(default=None, gt=0),
        min_price: float | None = Query(default=None, ge=0),
        max_price: float | None = Query(default=None, ge=0)
    ):
        self.search = search
        self.category_id = category_id
        self.min_price = min_price
        self.max_price = max_price


ProductFiltersDep = Annotated[ProductFilters, Depends()]

class SortingParams:
    def __init__(
        self,
        sort_by: ProductSortField = Query(default=ProductSortField.name),
        order: SortOrder = Query(default=SortOrder.asc)
    ):
        self.sort_by = sort_by
        self.order = order


SortingDep = Annotated[SortingParams, Depends()]

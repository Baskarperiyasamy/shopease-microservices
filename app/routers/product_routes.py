from typing import List, Optional

from fastapi import APIRouter, Path, Query, status

from app.config.settings import settings
from app.schemas.product_schema import (
    ErrorResponse,
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product_service import product_service

router = APIRouter(prefix="/api/products", tags=["Products"])

not_found = {404: {"model": ErrorResponse, "description": "Product not found"}}
bad_request = {400: {"model": ErrorResponse, "description": "Invalid request"}}
invalid_data = {422: {"model": ErrorResponse, "description": "Validation error"}}


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a product",
    responses={**bad_request, **invalid_data},
)
def create_product(product: ProductCreate):
    return product_service.create_product(product)


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Get all products",
    responses=invalid_data,
)
def get_products(
    category: Optional[str] = Query(default=None, description="Filter by category"),
    skip: int = Query(default=0, ge=0, description="Number of products to skip"),
    limit: int = Query(
        default=settings.default_page_limit,
        ge=1,
        le=settings.max_page_limit,
        description="Maximum number of products to return",
    ),
):
    return product_service.get_products(category=category, skip=skip, limit=limit)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get a product by ID",
    responses={**not_found, **bad_request, **invalid_data},
)
def get_product(product_id: int = Path(..., description="ID of the product")):
    return product_service.get_product(product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Update a product",
    responses={**not_found, **bad_request, **invalid_data},
)
def update_product(
    product: ProductUpdate,
    product_id: int = Path(..., description="ID of the product"),
):
    return product_service.update_product(product_id, product)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
    responses={**not_found, **bad_request, **invalid_data},
)
def delete_product(product_id: int = Path(..., description="ID of the product")):
    product_service.delete_product(product_id)

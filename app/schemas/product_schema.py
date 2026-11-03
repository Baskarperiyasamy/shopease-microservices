import re
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.product_model import ProductStatus

CATEGORY_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9 &'-]*$")


class ProductBase(BaseModel):
    name: str = Field(..., max_length=100, examples=["Wireless Mouse"])
    description: Optional[str] = Field(
        default=None, max_length=500, examples=["2.4 GHz ergonomic wireless mouse"]
    )
    price: float = Field(..., gt=0, le=10_000_000, examples=[799.0])
    stock_quantity: int = Field(..., ge=0, le=1_000_000, examples=[50])
    category: str = Field(..., min_length=2, max_length=50, examples=["Electronics"])
    status: ProductStatus = Field(default=ProductStatus.ACTIVE, examples=["Active"])

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Product name must not be empty")
        if not any(ch.isalnum() for ch in value):
            raise ValueError("Product name must contain meaningful text")
        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        return value or None

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Category must contain at least 2 characters")
        if not CATEGORY_PATTERN.match(value):
            raise ValueError(
                "Category must start with a letter and contain only letters, numbers, spaces, &, ' or -"
            )
        return value

    @field_validator("price")
    @classmethod
    def round_price(cls, value: float) -> float:
        return round(value, 2)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class ErrorDetail(BaseModel):
    field: str
    message: str


class ErrorResponse(BaseModel):
    status_code: int
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None

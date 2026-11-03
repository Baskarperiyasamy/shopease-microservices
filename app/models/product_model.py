from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ProductStatus(str, Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"


@dataclass
class Product:
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    category: str
    status: ProductStatus
    created_date: datetime

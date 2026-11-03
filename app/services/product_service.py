from datetime import datetime
from typing import Dict, List, Optional

from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class InvalidProductIdError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Invalid product ID {product_id}. Product ID must be a positive integer")


class DuplicateProductError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} already exists")


class ProductService:
    def __init__(self) -> None:
        self._products: Dict[int, Product] = {}
        self._next_id = 1

    def create_product(self, data: ProductCreate) -> Product:
        product_id = self._next_id
        if product_id in self._products:
            raise DuplicateProductError(product_id)

        product = Product(
            id=product_id,
            name=data.name,
            description=data.description,
            price=data.price,
            stock_quantity=data.stock_quantity,
            category=data.category,
            status=data.status,
            created_date=datetime.now(),
        )
        self._products[product_id] = product
        self._next_id += 1
        return product

    def get_products(
        self, category: Optional[str] = None, skip: int = 0, limit: int = 10
    ) -> List[Product]:
        products = list(self._products.values())
        if category:
            wanted = category.strip().lower()
            products = [p for p in products if p.category.lower() == wanted]
        return products[skip : skip + limit]

    def get_product(self, product_id: int) -> Product:
        self._check_id(product_id)
        product = self._products.get(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product

    def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        product = self.get_product(product_id)
        product.name = data.name
        product.description = data.description
        product.price = data.price
        product.stock_quantity = data.stock_quantity
        product.category = data.category
        product.status = data.status
        return product

    def delete_product(self, product_id: int) -> None:
        self.get_product(product_id)
        del self._products[product_id]

    @staticmethod
    def _check_id(product_id: int) -> None:
        if product_id <= 0:
            raise InvalidProductIdError(product_id)


product_service = ProductService()

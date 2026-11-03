import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config.settings import settings
from app.routers import product_routes
from app.services.product_service import (
    DuplicateProductError,
    InvalidProductIdError,
    ProductNotFoundError,
)

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Independent Product Management microservice for the ShopEase platform.",
    debug=settings.debug,
)

app.include_router(product_routes.router)


def error_response(status_code: int, error: str, message: str, details=None) -> JSONResponse:
    body = {"status_code": status_code, "error": error, "message": message}
    if details:
        body["details"] = details
    return JSONResponse(status_code=status_code, content=body)


@app.exception_handler(ProductNotFoundError)
async def product_not_found_handler(request: Request, exc: ProductNotFoundError):
    return error_response(404, "Not Found", str(exc))


@app.exception_handler(InvalidProductIdError)
async def invalid_product_id_handler(request: Request, exc: InvalidProductIdError):
    return error_response(400, "Bad Request", str(exc))


@app.exception_handler(DuplicateProductError)
async def duplicate_product_handler(request: Request, exc: DuplicateProductError):
    return error_response(400, "Bad Request", str(exc))


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()

    if any(err["type"] == "json_invalid" for err in errors):
        return error_response(400, "Bad Request", "Request body contains invalid JSON")

    details = []
    for err in errors:
        location = [str(part) for part in err["loc"] if part not in ("body", "query", "path")]
        message = err["msg"].removeprefix("Value error, ")
        details.append({"field": ".".join(location) or "request", "message": message})

    return error_response(422, "Validation Error", "Invalid request data", details)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    titles = {404: "Not Found", 405: "Method Not Allowed"}
    return error_response(exc.status_code, titles.get(exc.status_code, "Error"), str(exc.detail))


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    logger.exception("Unexpected error while handling %s %s", request.method, request.url.path)
    return error_response(500, "Internal Server Error", "An unexpected error occurred")


@app.get("/health", tags=["Health"], summary="Service health check")
def health_check():
    return {"status": "UP", "service": settings.app_name, "version": settings.app_version}

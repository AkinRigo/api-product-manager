from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.exceptions import ConflictError, NotFoundError
from app.routers.categories import router as categories_router
from app.routers.products import router as products_router
from app.routers.stock import router as stock_router

APP = FastAPI(title="Product Manager API")
APP.include_router(products_router)
APP.include_router(categories_router)
APP.include_router(stock_router)


@APP.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@APP.exception_handler(ConflictError)
@APP.exception_handler(IntegrityError)
async def conflict_handler(request: Request, exc: Exception):
    detail = str(exc) if isinstance(exc, ConflictError) else "Conflito com os dados enviados"
    return JSONResponse(status_code=409, content={"detail": detail})


@APP.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
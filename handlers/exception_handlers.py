from exceptions.base_exception import ApplicationException
from fastapi import Request
from fastapi.responses import JSONResponse
from schemas.response.error.error_schema import ErrorSchema
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)

async def api_exception_handler(request: Request, exc: ApplicationException) -> JSONResponse:
    logger.error("%s (status_code=%s)", exc.message, exc.status_code)
    error_schema = ErrorSchema(
        message=exc.message,
        status_code=exc.status_code
    )
    return JSONResponse(
        status_code=exc.status_code,
        content = error_schema.model_dump()  
    )

async def pydantic_request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Request validation error: %s", exc.errors())

    status_code = 422

    for error in exc.errors():
        error_message = error.get("msg")
        break

    error_schema = ErrorSchema(
        message=error_message,
        status_code=status_code
    )
    return JSONResponse(
        status_code=status_code,
        content = error_schema.model_dump()  
    )

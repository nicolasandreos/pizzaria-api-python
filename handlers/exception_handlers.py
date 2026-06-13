from exceptions.base_exception import BaseException
from fastapi import Request
from fastapi.responses import JSONResponse
from schemas.response.error.error_schema import ErrorSchema


async def api_exception_handler(request: Request, exc: BaseException) -> JSONResponse:
    error_schema = ErrorSchema(
        message=exc.message,
        status_code=exc.status_code
    )
    return JSONResponse(
        status_code=exc.status_code,
        content = error_schema.model_dump()  
    )

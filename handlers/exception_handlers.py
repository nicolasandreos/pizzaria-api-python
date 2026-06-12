from exceptions.base_exception import BaseException
from fastapi import Request
from fastapi.responses import JSONResponse


async def api_exception_handler(request: Request, exc: BaseException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message
        }
    )

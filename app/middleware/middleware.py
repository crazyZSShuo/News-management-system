from fastapi import Request
from fastapi.responses import JSONResponse
from app.exception import NewsException
import time
from typing import Callable
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def catch_exceptions_middleware(request: Request, call_next: Callable):
    try:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request processed in {process_time:.2f} seconds")
        return response
    except NewsException as exc:
        logger.error(f"NewsException: {exc.detail['message']}", exc_info=True)
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.detail["code"],
                "message": exc.detail["message"]
            }
        )
    except Exception as exc:
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "code": 50000,
                "message": "Internal server error"
            }
        )
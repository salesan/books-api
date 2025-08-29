from starlette.middleware.base import BaseHTTPMiddleware
import time
from logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(
            "Request processed",
            extra={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "duration": round(process_time, 4),
                "client": request.client.host,
            },
        )
        return response

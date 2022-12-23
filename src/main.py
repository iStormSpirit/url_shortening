import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from api import base
from core import config
from core.config import logger

app = FastAPI(
    title=config.app_settings.app_title,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(base.api_router)


@app.middleware('http')
async def validate_ip(request: Request, call_next):
    ip = str(request.client.host)
    logger.info(f'request_ip: {ip}')
    if ip in config.app_settings.Config.BLOCKED_IPS:
        data = {
            'message': f'IP {ip} is not allowed to access this resource.'
        }
        return ORJSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=data)
    return await call_next(request)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=config.PROJECT_HOST,
        port=config.PROJECT_PORT,
    )

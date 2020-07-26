from fastapi import FastAPI
import logging

from api_composition_proxy.routers import get_proxy, post_proxy, health
from api_composition_proxy.configurations import _FastAPIConfigurations, _PlatformConfigurations

logger = logging.getLogger(__name__)
logger.info(
    f'starts {_FastAPIConfigurations().title}:{_FastAPIConfigurations().version}')
logger.info(f'platform: {_PlatformConfigurations().platform}')

app = FastAPI(
    title=_FastAPIConfigurations().title,
    description=_FastAPIConfigurations().description,
    version=_FastAPIConfigurations().version,
)


app.include_router(
    health.router,
    prefix='/health',
    tags=['health']
)

app.include_router(
    get_proxy.router,
    prefix='/get_redirect',
    tags=['get_redirect']
)

app.include_router(
    post_proxy.router,
    prefix='/post_redirect',
    tags=['post_redirect']
)

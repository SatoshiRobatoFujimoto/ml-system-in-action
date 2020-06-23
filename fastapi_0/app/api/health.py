from fastapi import APIRouter
from . import _health
import logging

logger = logging.getLogger(__name__) 
router = APIRouter()


@router.get("/")
def health():
    return _health.health()


@router.get("/sync")
def health_sync():
    return _health.health_sync()


@router.get("/async")
async def health_async():
    return _health.health_async()

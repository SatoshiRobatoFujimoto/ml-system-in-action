from fastapi import APIRouter, BackgroundTasks
import logging

from . import _predict
from app.ml.active_predictor import Data

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('')
def test():
    prediction = _predict.test()
    return prediction


@router.post('')
def predict(data: Data,
            background_tasks: BackgroundTasks):
    prediction = _predict.predict(data, background_tasks)
    return prediction


@router.post('/async')
async def predict_async(data: Data,
                        background_tasks: BackgroundTasks):
    job_id = await _predict.predict_async_post(data, background_tasks)
    return job_id


@router.get('/async/{job_id}')
def predict_async(job_id: str):
    return _predict.predict_async_get(job_id)

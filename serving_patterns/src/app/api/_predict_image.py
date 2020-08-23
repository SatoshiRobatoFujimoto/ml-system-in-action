from typing import Dict, List
from fastapi import BackgroundTasks
import logging
from PIL import Image
import io
import numpy as np
import base64

from src.middleware.profiler import do_cprofile
from src.jobs import store_data_job
from src.helper import get_image_data
from src.app.ml.active_predictor import Data, DataConverter, active_predictor
from src.app.api import _predict as _parent_predict

logger = logging.getLogger(__name__)


@do_cprofile
def __predict(data: Data):
    image_data = get_image_data(data.image_data)
    output_np = active_predictor.predict(image_data)
    reshaped_output_nps = DataConverter.reshape_output(output_np)
    data.prediction = reshaped_output_nps.tolist()
    logger.info({'job_id': data.job_id, 'prediction': data.prediction})


@do_cprofile
def __predict_label(data: Data) -> Dict[str, float]:
    return _parent_predict.__predict_label(data, __predict)


@do_cprofile
async def __async_predict(data: Data):
    image_data = get_image_data(data.image_data)
    output_np = await active_predictor.async_predict(image_data)
    reshaped_output_nps = DataConverter.reshape_output(output_np)
    data.prediction = reshaped_output_nps.tolist()
    logger.info({'job_id': data.job_id, 'prediction': data.prediction})


@do_cprofile
async def __async_predict_label(data: Data) -> Dict[str, float]:
    return await _parent_predict.__async_predict_label(data, __async_predict)


def _predict_from_redis_cache(job_id: str,
                              data_class: callable = Data) -> Data:
    data_dict = store_data_job.load_data_redis(job_id)
    if data_dict is None:
        return None
    if 'image_data' in data_dict.keys():
        image_key = store_data_job.make_image_key(job_id)
        if isinstance(data_dict['image_data'], str) and data_dict['image_data'] == image_key:
            image_data = store_data_job.get_image_redis(image_key)
            data_dict['image_data'] = image_data
    data = data_class(**data_dict)
    __predict(data)
    return data


def _labels(data_class: callable = Data) -> Dict[str, List[str]]:
    return _parent_predict._labels(data_class)


def _test(data: Data = Data()) -> Dict[str, int]:
    data.image_data = data.test_data
    return _parent_predict._test(data, __predict)


def _test_label(data: Data = Data()) -> Dict[str, Dict[str, float]]:
    data.image_data = data.test_data
    return _parent_predict._test_label(data, __predict_label)


async def _predict(
        data: Data,
        job_id: str,
        background_tasks: BackgroundTasks = BackgroundTasks()) -> Dict[str, List[float]]:
    image = base64.b64decode(str(data.image_data))
    io_bytes = io.BytesIO(image)
    data.image_data = Image.open(io_bytes)
    await __async_predict(data)
    store_data_job._save_data_job(data, job_id, background_tasks, False)
    return {'prediction': data.prediction, 'job_id': job_id}


async def _predict_label(
        data: Data,
        job_id: str,
        background_tasks: BackgroundTasks = BackgroundTasks()) -> Dict[str, List[float]]:
    image = base64.b64decode(str(data.image_data))
    io_bytes = io.BytesIO(image)
    data.image_data = Image.open(io_bytes)
    label_proba = await __async_predict_label(data)
    store_data_job._save_data_job(data, job_id, background_tasks, False)
    return {'prediction': label_proba, 'job_id': job_id}


async def _predict_async_post(
        data: Data,
        job_id: str,
        background_tasks: BackgroundTasks = BackgroundTasks()) -> Dict[str, List[float]]:
    image = base64.b64decode(str(data.image_data))
    io_bytes = io.BytesIO(image)
    data.image_data = Image.open(io_bytes)
    store_data_job._save_data_job(data, job_id, background_tasks, True)
    return {'job_id': job_id}


def _predict_async_get(job_id: str) -> Dict[str, List[float]]:
    return _parent_predict._predict_async_get(job_id)


def _predict_async_get_label(
        job_id: str) -> Dict[str, Dict[str, Dict[str, float]]]:
    return _parent_predict._predict_async_get_label(job_id)

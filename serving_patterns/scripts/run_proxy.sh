#!/bin/bash

set -eu

GUNICORN_UVICORN=${GUNICORN_UVICORN:-"GUNICORN"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8888}
WORKERS=${WORKERS:-4}
UVICORN_WORKER=${UVICORN_WORKER:-"uvicorn.workers.UvicornWorker"}
LOGLEVEL=${LOGLEVEL:-"debug"}
LOGCONFIG=${LOGCONFIG:-"./logging/logging.conf"}
BACKLOG=${BACKLOG:-2048}
LIMIT_MAX_REQUESTS=${LIMIT_MAX_REQUESTS:-65536}
MAX_REQUESTS_JITTER=${MAX_REQUESTS_JITTER:-2048}
APP_NAME=${APP_NAME:-"src.api_composition_proxy.apps.proxy:app"}


if [ ${GUNICORN_UVICORN} = "GUNICORN" ]; then
    gunicorn ${APP_NAME} \
        -b ${HOST}:${PORT} \
        -w ${WORKERS} \
        -k ${UVICORN_WORKER}  \
        --log-level ${LOGLEVEL} \
        --log-config ${LOGCONFIG} \
        --backlog ${BACKLOG} \
        --max-requests ${LIMIT_MAX_REQUESTS} \
        --max-requests-jitter ${MAX_REQUESTS_JITTER} \
        --reload

else
    uvicorn ${APP_NAME} \
        --host ${HOST} \
        --port ${PORT} \
        --workers ${WORKERS} \
        --log-level ${LOGLEVEL} \
        --log-config ${LOGCONFIG} \
        --backlog ${BACKLOG} \
        --limit-max-requests ${LIMIT_MAX_REQUESTS} \
        --reload
fi
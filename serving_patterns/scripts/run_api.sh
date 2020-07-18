#!/bin/bash

set -eu

GUNICORN_UVICORN=${GUNICORN_UVICORN:-"GUNICORN"}
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8888}
WORKERS=${WORKERS:-4}
UVICORN_WORKER=${UVICORN_WORKER:-"uvicorn.workers.UvicornWorker"}
LOGLEVEL=${LOGLEVEL:-"debug"}
LOGCONFIG=${LOGCONFIG:-"./app/logging.conf"}
APP_NAME=${APP_NAME:-"app.apps.app_web_single"}


if [ ${GUNICORN_UVICORN} = "GUNICORN" ]; then
    gunicorn ${APP_NAME}:app \
        -b ${HOST}:${PORT} \
        -w ${WORKERS} \
        -k ${UVICORN_WORKER}  \
        --log-level ${LOGLEVEL} \
        --log-config ${LOGCONFIG}

else
    uvicorn ${APP_NAME}:app \
        --host ${HOST} \
        --port ${PORT} \
        --workers ${WORKERS} \
        --log-level ${LOGLEVEL} \
        --log-config ${LOGCONFIG}
fi
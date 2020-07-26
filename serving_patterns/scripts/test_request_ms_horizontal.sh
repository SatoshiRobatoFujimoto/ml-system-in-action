#!/bin/bash

set -eu

TARGET_HOST=localhost
PORT=8000
HEALTH=health
GET_REDIRECT=get_redirect
POST_REDIRECT=post_redirect
LABELS=labels
PREDICT=predict
LABEL=label
ASYNC=async
JSON_PATH=./app/ml/data/good_cat_base64_data.json

function which_is_it() {
    echo "******* ${1} *******"
}

function finish() {
    echo -e "\n"
}

function health() {
    endpoint=${TARGET_HOST}:$1/${HEALTH}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function health_all() {
    endpoint=${TARGET_HOST}:$1/${GET_REDIRECT}/${HEALTH}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function labels(){
    endpoint=${TARGET_HOST}:$1/${GET_REDIRECT}/${PREDICT}/${LABELS}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function test_predict() {
    endpoint=${TARGET_HOST}:$1/${GET_REDIRECT}/${PREDICT}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function test_predict_label() {
    endpoint=${TARGET_HOST}:$1/${GET_REDIRECT}/${PREDICT}/${LABEL}
    which_is_it "${endpoint}"
    curl -X GET \
        ${endpoint}
    finish
}

function predict() {
    endpoint=${TARGET_HOST}:$1/${POST_REDIRECT}/${PREDICT}
    which_is_it "${endpoint}"
    curl -X POST \
        -H "Content-Type: application/json" \
        -d @${JSON_PATH} \
        ${endpoint}
    finish
}

function predict_label() {
    endpoint=${TARGET_HOST}:$1/${POST_REDIRECT}/${PREDICT}/${LABEL}
    which_is_it "${endpoint}"
    curl -X POST \
        -H "Content-Type: application/json" \
        -d @${JSON_PATH} \
        ${endpoint}
    finish
}

function predict_async() {
    endpoint=${TARGET_HOST}:$1/${POST_REDIRECT}/${PREDICT}/${ASYNC}
    which_is_it "${endpoint}"
    curl -X POST \
        -H "Content-Type: application/json" \
        -d @${JSON_PATH} \
        ${endpoint}
    finish
}

function all() {
    health $1
    health_all $1
    labels $1
    test_predict $1
    test_predict_label $1
    predict $1
    predict_label $1
    predict_async $1
}

all ${PORT}
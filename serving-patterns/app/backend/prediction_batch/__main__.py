import logging
import asyncio

from app.backend.prediction_batch.prediction_batch import prediction_loop


log_format = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
logger = logging.getLogger('prediction_batch')
stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(log_format)
logger.addHandler(stdout_handler)
logger.setLevel(logging.DEBUG)


def main():
    prediction_loop()


if __name__ == '__main__':
    logger.info('start backend')
    main()

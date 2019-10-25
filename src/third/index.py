import logging
import os
from urllib.parse import unquote_plus
import json

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    print(json.dumps(event))
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logger.setLevel(log_level)

    for record in event['Records']:
        received_message = unquote_plus(record['body'])
        logger.debug("received message: {}".format(received_message))
        message = "This is third, no further sending to queu, just logging.\n{}".format(received_message)
        logger.info(message)


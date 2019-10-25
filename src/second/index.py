import logging
import os
from urllib.parse import quote_plus, unquote_plus
import boto3
import json

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    print(json.dumps(event))
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    queue = os.environ.get('OUTPUT_QUEUE')
    logger.setLevel(log_level)

    for record in event['Records']:
        received_message = unquote_plus(record['body'])
        logger.debug("received message: {}".format(received_message))
        message = "This is second, sending the following message to third.\n{}".format(received_message)
        if queue:
            sqs_client = boto3.client('sqs')
            response = sqs_client.send_message(
                QueueUrl=queue,
                MessageBody=quote_plus(message)
            )
            logger.debug("send to queue: {}\n{}".format(queue, response))
        else:
            logger.error('no OUTPUT_QUEUE defined, can not send to next queue.')

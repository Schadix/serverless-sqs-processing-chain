import boto3
import json
import argparse

parser = argparse.ArgumentParser('Reads through file with one json per line and pushes messages to SQS')
parser.add_argument('--sqs-url', required=True)
parser.add_argument('--messages-file', required=True)
parser.add_argument('--profile', required=False)

args=parser.parse_args()

if args.profile:
    boto_session = boto3.session.Session(profile_name=args.profile)
    client = boto_session.client('sqs', )
else:
    client = boto3.client('sqs')

queue_url = args.sqs_url
messages_file = args.messages_file

message_number = 0
entries = []

with open(messages_file) as messages_input_file:
    for message in messages_input_file:
        message = json.loads(message)
        print(message)
        entry = {
            'Id': str("{}".format(message_number)),
            'MessageBody': json.dumps(message),
            'DelaySeconds': 0
        }
        message_number += 1
        entries.append(entry)
        if len(entries) == 10:
            response = client.send_message_batch(
                QueueUrl=queue_url,
                Entries=entries
            )
            entries = []
if entries:
    response = client.send_message_batch(
        QueueUrl=queue_url,
        Entries=entries
    )
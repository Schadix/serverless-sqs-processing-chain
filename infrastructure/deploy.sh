#!/usr/bin/env bash
set -e

if [[ $# -ne 1 ]]; then
  echo "Usage $0 <s3-bucket> "
  exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd "${DIR}"

S3_BUCKET=$1
TEMPLATE_NAME=cloudformation
STACK_NAME=sqs-processing

# DEPLOY
sam build --template ${TEMPLATE_NAME}.yaml

sam package --s3-bucket ${S3_BUCKET} --s3-prefix ${TEMPLATE_NAME} --output-template-file ${TEMPLATE_NAME}-packaged.yaml

sam deploy --template-file ./${TEMPLATE_NAME}-packaged.yaml --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM --no-fail-on-empty-changeset

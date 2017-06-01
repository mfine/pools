#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
import uuid

def main():
    client = boto3.client('swf')
    uid = uuid.uuid4()
    print uid
    try:
        client.start_workflow_execution(
            domain = 'pools',
            workflowId = str(uid),
            workflowType = {'name': 'workflow', 'version': '1.1'},
            taskList = {'name': 'workflow'},
            executionStartToCloseTimeout = '31536000',
            taskStartToCloseTimeout = '15',
            childPolicy = 'ABANDON',
        )
    except ClientError as e:
        raise

if __name__ == "__main__":
    main()

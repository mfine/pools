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
            domain = 'loops',
            workflowId = str(uid),
            workflowType = {'name': 'workflow', 'version': '1.2'},
            taskList = {'name': 'workflow'},
            executionStartToCloseTimeout = '604800',
            taskStartToCloseTimeout = 'NONE',
            childPolicy = 'ABANDON',
        )
    except ClientError as e:
        raise

if __name__ == "__main__":
    main()

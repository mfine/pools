#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
import sys

def main():
    client = boto3.client('swf')
    try:
        client.request_cancel_workflow_execution(
            domain = 'loops',
            workflowId = sys.argv[1],
        )
    except ClientError as e:
        raise


if __name__ == "__main__":
    main()



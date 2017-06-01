#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError

def main():
    client = boto3.client('swf')
    try:
        client.register_domain(
            name = 'pools',
            workflowExecutionRetentionPeriodInDays = 'NONE',
        )
    except ClientError as e:
        if e.response['Error']['Code'] != 'DomainAlreadyExistsFault':
            raise
    try:
        client.register_workflow_type(
            domain = 'pools',
            name = 'workflow',
            version = '1.1',
            defaultTaskStartToCloseTimeout = '15',
            defaultExecutionStartToCloseTimeout = '31536000',
        )
    except ClientError as e:
        if e.response['Error']['Code'] != 'TypeAlreadyExistsFault':
            raise
    try:
        client.register_activity_type(
            domain = 'pools',
            name = 'activity',
            version = '1.1',
            defaultTaskStartToCloseTimeout = 'NONE',
            defaultTaskScheduleToStartTimeout = '15',
            defaultTaskScheduleToCloseTimeout = 'NONE',
            defaultTaskHeartbeatTimeout = '15',
        )
    except ClientError as e:
        if e.response['Error']['Code'] != 'TypeAlreadyExistsFault':
            raise

if __name__ == "__main__":
    main()

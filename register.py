#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError

def main():
    client = boto3.client('swf')
    try:
        client.register_domain(
            name = 'loops',
            workflowExecutionRetentionPeriodInDays = 'NONE',
        )
    except ClientError as e:
        if e.response['Error']['Code'] != 'DomainAlreadyExistsFault':
            raise
    try:
        client.register_workflow_type(
            domain = 'loops',
            name = 'workflow',
            version = '1.4',
            defaultTaskStartToCloseTimeout = 'NONE',
            defaultExecutionStartToCloseTimeout = '604800',
        )
    except ClientError as e:
        if e.response['Error']['Code'] != 'TypeAlreadyExistsFault':
            raise
    try:
        client.register_activity_type(
            domain = 'loops',
            name = 'activity',
            version = '1.4',
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

#!/usr/bin/env python

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import sys

def main():
    config = Config(connect_timeout=70, read_timeout=70)
    client = boto3.client('swf', config=config)
    while True:
        try:
            task = client.poll_for_activity_task(
                domain = 'loops',
                taskList = {'name': 'activity'},
            )
            if 'taskToken' in task:
                print task['workflowExecution']['workflowId']
                client.respond_activity_task_completed(
                    taskToken = task['taskToken'],
                )
        except ClientError as e:
            raise
        except KeyboardInterrupt:
            sys.exit(-1)

if __name__ == "__main__":
    main()

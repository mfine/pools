#!/usr/bin/env python

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import sys
import time
import json

def main():
    config = Config(connect_timeout=70, read_timeout=70)
    client = boto3.client('swf', config=config)
    while True:
        try:
            print "------"
            task = client.poll_for_activity_task(
                domain = 'pools',
                taskList = {'name': 'activity'},
            )
            if 'taskToken' in task:
                canceled = False
                while True:
                    print "%s with %s" % (task['workflowExecution']['workflowId'], json.loads(task['input']))
                    time.sleep(5.0)
                    response = client.record_activity_task_heartbeat(
                        taskToken = task['taskToken'],
                    )
                    del response['ResponseMetadata']
                    if response:
                        print response
                    if response['cancelRequested'] == True:
                        canceled = True
                        response = client.respond_activity_task_canceled(
                            taskToken = task['taskToken'],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                        break
                if not canceled:
                    response = client.respond_activity_task_completed(
                        taskToken = task['taskToken'],
                    )
                    del response['ResponseMetadata']
                    if response:
                        print response
        except ClientError as e:
            raise
        except KeyboardInterrupt:
            sys.exit(-1)

if __name__ == "__main__":
    main()

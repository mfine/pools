#!/usr/bin/env python

import boto3
from botocore.exceptions import ClientError
import sys
import yaml
import datetime

def main():
    with open(sys.argv[1], 'r') as f:
        items = yaml.load(f)
        client = boto3.client('swf')
        try:
            response = client.list_open_workflow_executions(
                domain = 'pools',
                startTimeFilter = {'oldestDate': datetime.datetime(1970, 1, 1)},
                typeFilter = {'name': 'workflow', 'version': '1.1'},
            )
            del response['ResponseMetadata']
            if response:
                flows = [flow['execution']['workflowId'] for flow in response['executionInfos'] if flow['cancelRequested'] == False]
                adds = [i for i in items.keys() if i not in flows]
                dels = [f for f in flows if f not in items.keys()]
                for a in adds:
                    input = items[a]['input']
                    print "Starting %s with %s" % (a, input)
                    try:
                        client.start_workflow_execution(
                            domain = 'pools',
                            workflowId = a,
                            workflowType = {'name': 'workflow', 'version': '1.1'},
                            taskList = {'name': 'workflow'},
                            executionStartToCloseTimeout = '31536000',
                            taskStartToCloseTimeout = 'NONE',
                            childPolicy = 'ABANDON',
                            input = input,
                        )
                    except ClientError as e:
                        if e.response['Error']['Code'] != 'UnknownResourceFault':
                            raise
                for d in dels:
                    print "Stopping %s" % d
                    try:
                        client.request_cancel_workflow_execution(
                            domain = 'pools',
                            workflowId = d,
                        )
                    except ClientError as e:
                        if e.response['Error']['Code'] != 'UnknownResourceFault':
                            raise
        except ClientError as e:
            raise

if __name__ == "__main__":
    main()



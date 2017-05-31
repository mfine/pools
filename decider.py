#!/usr/bin/env python

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import sys
import uuid

def main():
    config = Config(connect_timeout=70, read_timeout=70)
    client = boto3.client('swf', config=config)
    while True:
        try:
            task = client.poll_for_decision_task(
                domain = 'pools',
                taskList = {'name': 'workflow'},
            )
            if 'taskToken' in task:
                if 'events' in task:
                    history = [event for event in task['events'] if not event['eventType'].startswith('Decision')]
                    last = history[-1]
                    if last['eventType'] == 'WorkflowExecutionStarted':
                        print 'WorkflowExecutionStarted'
                        uid = uuid.uuid4()
                        print uid
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                                { 'decisionType': 'ScheduleActivityTask',
                                  'scheduleActivityTaskDecisionAttributes': {
                                      'activityType': {'name': 'activity', 'version': '1.0'},
                                      'taskList': {'name': 'activity'},
                                      'activityId': str(uid),
                                  },
                                },
                            ],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    elif last['eventType'] == 'ActivityTaskCompleted':
                        print 'ActivityTaskCompleted'
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                              { 'decisionType': 'CompleteWorkflowExecution',
                                'completeWorkflowExecutionDecisionAttributes': {
                                },
                              },
                            ],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    elif last['eventType'] == 'ActivityTaskTimedOut':
                        print 'ActivityTaskTimedOut'
                        uid = uuid.uuid4()
                        print uid
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                                { 'decisionType': 'ScheduleActivityTask',
                                  'scheduleActivityTaskDecisionAttributes': {
                                      'activityType': {'name': 'activity', 'version': '1.0'},
                                      'taskList': {'name': 'activity'},
                                      'activityId': str(uid),
                                  },
                                },
                            ],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    elif last['eventType'] == 'WorkflowExecutionCancelRequested':
                        print 'WorkflowExecutionCancelRequested'
                        history1 = [event for event in task['events'] if event['eventType'] == 'ActivityTaskScheduled']
                        last1 = history1[-1]
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                                { 'decisionType': 'RequestCancelActivityTask',
                                  'requestCancelActivityTaskDecisionAttributes': {
                                      'activityId': last1['activityTaskScheduledEventAttributes']['activityId'],
                                  },
                                },
                            ],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    elif last['eventType'] == 'ActivityTaskCanceled':
                        print 'ActivityTaskCanceled'
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                                { 'decisionType': 'CompleteWorkflowExecution',
                                  'completeWorkflowExecutionDecisionAttributes': {
                                  },
                                },
                            ],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    else:
                        print 'UNKNOWN'
                        print last
        except ClientError as e:
            raise
        except KeyboardInterrupt:
            sys.exit(-1)


if __name__ == "__main__":
    main()

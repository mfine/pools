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
            print "------"
            task = client.poll_for_decision_task(
                domain = 'pools',
                taskList = {'name': 'workflow'},
                reverseOrder = True,
            )
            if 'taskToken' in task:
                if 'events' in task:
                    history = [event for event in task['events'] if not event['eventType'].startswith('Decision')]
                    print task['events']
                    last = history[0]
                    if last['eventType'] == 'WorkflowExecutionStarted':
                        print 'WorkflowExecutionStarted'
                        uid = uuid.uuid4()
                        print uid
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                                { 'decisionType': 'ScheduleActivityTask',
                                  'scheduleActivityTaskDecisionAttributes': {
                                      'activityType': {'name': 'activity', 'version': '1.1'},
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
                                      'activityType': {'name': 'activity', 'version': '1.1'},
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
                        last1 = history1[0]
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
                    elif last['eventType'] == 'ActivityTaskScheduled':
                        print '*** ActivityTaskScheduled ***'
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    elif last['eventType'] == 'ActivityTaskStarted':
                        print '*** ActivityTaskStarted ***'
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    elif last['eventType'] == 'RequestCancelActivityTaskFailed':
                        print '*** RequestCancelActivityTaskFailed ***'
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                                { 'decisionType': 'FailWorkflowExecution',
                                  'failWorkflowExecutionDecisionAttributes': {
                                  },
                                },
                            ],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    elif last['eventType'] == 'FailWorkflowExecutionFailed':
                        print '*** FailWorkflowExecutionFailed ***'
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [],
                        )
                        del response['ResponseMetadata']
                        if response:
                            print response
                    else:
                        print 'UNKNOWN'
                        print last
                        response = client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [],
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

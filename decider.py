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
                domain = 'loops',
                taskList = {'name': 'workflow'},
            )
            if 'taskToken' in task:
                if 'events' in task:
                    history = [event for event in task['events'] if not event['eventType'].startswith('Decision')]
                    last = history[-1]
                    if last['eventType'] == 'WorkflowExecutionStarted':
                        uid = uuid.uuid4()
                        print uid
                        client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                                { 'decisionType': 'ScheduleActivityTask',
                                  'scheduleActivityTaskDecisionAttributes': {
                                      'activityType': {'name': 'activity', 'version': '1.2'},
                                      'taskList': {'name': 'activity'},
                                      'activityId': str(uid),
                                  },
                                },
                            ],
                        )
                    elif last['eventType'] == 'ActivityTaskCompleted':
                        client.respond_decision_task_completed(
                            taskToken = task['taskToken'],
                            decisions = [
                              { 'decisionType': 'CompleteWorkflowExecution',
                                'completeWorkflowExecutionDecisionAttributes': {
                                },
                              },
                            ],
                        )
        except ClientError as e:
            raise
        except KeyboardInterrupt:
            sys.exit(-1)


if __name__ == "__main__":
    main()

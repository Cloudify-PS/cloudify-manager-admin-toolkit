import argparse
import datetime
import json

from itsdangerous import base64_encode
from collections import OrderedDict
from cloudify_rest_client.client import CloudifyClient

TASK_EVENTS = ['task_started', 'sending_task', 'task_rescheduled', 'task_succeeded', 'task_failed']
TASK_ENDED_EVENTS = ['task_succeeded', 'task_failed', 'task_rescheduled']

parser = argparse.ArgumentParser()
parser.add_argument("--host", required=True)
parser.add_argument("--port", default=80)
parser.add_argument("--user")
parser.add_argument("--password")
parser.add_argument("-e", required=True)

args = parser.parse_args()

if args.user:
    credentials = '{0}:{1}'.format(args.user, args.password)
    headers = {
        "Authorization":
            "Basic" + ' ' + base64_encode(credentials)}
else:
    headers = None

client = CloudifyClient(host=args.host, port=args.port, headers=headers)
execution_id = args.e

events_client = client.events
executions_client = client.executions
blueprints_client = client.blueprints

execution_info = executions_client.get(execution_id)
blueprint_id = execution_info['blueprint_id']
blueprint_info = blueprints_client.get(blueprint_id)

# Create a node_id -> node info map (needed because, in blueprint_info,
# the nodes are arranged in a list, rather than a dict.

nodes_info = {}

for node in blueprint_info['plan']['nodes']:
    nodes_info[node['id']] = node

events = events_client.list(execution_id=execution_id)

tasks_info = OrderedDict()
for event in events:
    event_type = event['event_type']
    if not event_type in TASK_EVENTS:
        continue
    event_context = event['context']
    task_id = event_context['task_id']
    node_name = event_context.get('node_name')
    operation = event_context['operation']

    if node_name:
        node_info = nodes_info[node_name]
        operation_info = node_info['operations'][operation]
        implementation = operation_info['operation']
        inputs = operation_info['inputs']
    else:
        # This is a relationship operation. Until CFY-6566 is resolved, we can't tell
        # whether we're running on the source or on the target.
        implementation = '<unknown>'
        inputs = '<unknown>'

    if task_id in tasks_info:
        task_info = tasks_info[task_id]
    else:
        task_info = OrderedDict({'node_name': event_context.get('node_name'),
                                 'source_name': event_context.get('source_name'),
                                 'target_name': event_context.get('target_name'),
                                 'operation': operation,
                                 'implementation': implementation,
                                 'inputs': inputs,
                                 'node_id': event_context.get('node_id'),
                                 'source_id': event_context.get('source_id'),
                                 'target_id': event_context.get('target_id'),
                                 'events': []})
        tasks_info[task_id] = task_info

    task_info['events'].append(OrderedDict({
        'timestamp': event['timestamp'],
        'event': event['event_type']}))

# Sort events

for _, task_info in tasks_info.iteritems():
    task_info['events'] = sorted(task_info['events'], key=lambda x: x['timestamp'])

# Find unfinished tasks

unfinished_tasks = []

def parse_event_ts(ts):
    # For some reason, %z doesn't work for me in the format string.
    # So I'm cutting the last 5 characters of the string.
    return datetime.datetime.strptime(ts['timestamp'][:-5], '%Y-%m-%d %H:%M:%S.%f')


for task_id, task_info in tasks_info.iteritems():
    task_events = task_info['events']
    first_event = task_events[0]
    last_event = task_events[-1]
    total_time = parse_event_ts(last_event) - parse_event_ts(first_event)

    print 'Task: {} ({}, {}): {} seconds'.format(task_id,
                                                 task_info.get('node_id') or '{}->{}'.format(task_info['source_id'], task_info['target_id']),
                                                 task_info.get('operation'),
                                                 total_time.total_seconds())
    print '    Implementation: {}'.format(task_info['implementation'])
    print '    Inputs: {}'.format(json.dumps(task_info['inputs']))
    print '    Events:'
    for event in task_events:
        print '        {}: {}'.format(event['timestamp'], event['event'])

    if last_event.get('event') not in TASK_ENDED_EVENTS:
        unfinished_tasks.append((task_id, task_info))

if len(unfinished_tasks) > 0:
    print "Unfinished tasks:"
    print "-----------------\n"
    print json.dumps(unfinished_tasks, indent=True)
else:
    print "No unfinished tasks"

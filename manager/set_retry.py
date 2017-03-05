#! /usr/bin/env python
import os
import sys
import base64
from cloudify_rest_client import CloudifyClient
import yaml


def get_auth_header(username, password):


    headers = {}

    headers.update({'Authorization':
                    'Basic ' + base64.b64encode('{0}:{1}'.format(
                        username, password))})
    return headers


def mod_retry_context(managerhost,username,password,task_retries,task_retry_interval):
    auth_header = get_auth_header( username, password )


    c = CloudifyClient( managerhost , headers=auth_header )

    name = c.manager.get_context()['name']
    context = c.manager.get_context()['context']


    print "Originalk workflow context {} " . format(context['cloudify']['workflows'])

    context['cloudify']['workflows']['task_retries'] = task_retries
    context['cloudify']['workflows']['task_retry_interval'] = task_retry_interval

    print "Updated workflow Context {} " . format(context['cloudify']['workflows'])

    print('Updating context')

    c.manager.update_context(name, context)


if __name__ == '__main__':

    if len(sys.argv) > 4:

        managerhost =  sys.argv[1]
        managerhost =  sys.argv[1]
        username =  sys.argv[2]
        password = sys.argv[3]
        task_retries = sys.argv[4]
        task_retry_interval = sys.argv[5]

        mod_retry_context(managerhost, username , password , task_retries, task_retry_interval)

    else:
       print "Usage: \n set_retry.py  Manager Username Password task_retries task_retry_interval "

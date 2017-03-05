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


def get_context(managerhost,username,password):
    auth_header = get_auth_header( username, password )


    c = CloudifyClient( managerhost , headers=auth_header )

    name = c.manager.get_context()['name']
    context = c.manager.get_context()['context']


    print "Original context {} " . format(context['cloudify'])



if __name__ == '__main__':

    if len(sys.argv) > 2:

        managerhost =  sys.argv[1]
        username =  sys.argv[2]
        password = sys.argv[3]
      
        
    
        get_context(managerhost, username , password )

    else:
       print "Usage: \n get_context.py  ManagerIP Username Password "

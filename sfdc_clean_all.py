#!/usr/bin/python
#    Copyright 2016 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Configure the Nagios server with the CGI service for passive checks.
# Configure virtual hosts for monitoring the clusters of global services and nodes
#



import logging
import os
import sys
import yaml
import json
# import shutil
import socket

from argparse import ArgumentParser
from salesforce import OAuth2, Client


LOG = None

def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config-file', default='config.yml')


    parser.add_argument('--syslog', action='store_true', default=False,
                           help='Log to syslog')

    parser.add_argument('--debug', action='store_true', default=False,
                           help='Enable debug log level')

    parser.add_argument('--log_file', default=sys.stdout,
                           help='Log file. default: stdout. Ignored if logging configured to syslog')



    args = parser.parse_args()

    LOG = logging.getLogger()
    if args.syslog:
        handler = logging.SysLogHandler()
    elif (args.log_file != sys.stdout ):
        handler = logging.FileHandler(args.log_file)
    else:
        handler = logging.StreamHandler(sys.stdout)

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    formatter = logging.Formatter(
        '{} nagios_to_sfdc %(asctime)s %(process)d %(levelname)s %(name)s '
        '[-] %(message)s'.format(socket.getfqdn()),
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    LOG.setLevel(log_level)
    LOG.addHandler(handler)


    with open(args.config_file) as fp:
        config = yaml.load(fp)
    
    if 'sfdc_organization_id' in config:
        organizationId = config['sfdc_organization_id']
    else:
        organizationId = None

    sfdc_oauth2 = OAuth2(client_id = config['sfdc_client_id'],
                         client_secret = config['sfdc_client_secret'],
                         username = config['sfdc_username'],
                         password = config['sfdc_password'],
                         auth_url = config['sfdc_auth_url'],
                         organizationId = organizationId )


    sfdc_client = Client(sfdc_oauth2)
    
# Serach example
#    a=sfdc_client.search("SELECT Id from Case")
#    for b  in a:
#        print(b['Id'])
#        sfdc_client.get_case(b['Id'])


    a=sfdc_client.search("SELECT Id from MOS_Alerts__c")
    for b  in a:
        print(b['Id'])
        alert = sfdc_client.get_mos_alert(b['Id'])
        print(json.dumps(alert.json(), sort_keys=True, indent=4, separators=(',', ': ') ))
        sfdc_client.del_mos_alert(b['Id'])

    a = sfdc_client.search("SELECT Id from MOS_Alert_Comment__c")
    for b  in a:
        print(b['Id'])
        a = sfdc_client.del_mos_alert_comment(b['Id'])
#        alert = sfdc_client.get_mos_alert_comment(b['Id'])
#        print(json.dumps(alert.json(), sort_keys=True, indent=4, separators=(',', ': ') ))
        #print(a.status_code)
        print(a.text)

if __name__ == '__main__':
    main()


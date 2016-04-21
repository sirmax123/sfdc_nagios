import logging
import os
import sys
import yaml
import json
# import shutil

from jsb import LOG
from argparse import ArgumentParser
from salesforce import OAuth2, Client




def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--config-file', default='config.yml')
    parser.add_argument('-d', '--debug', action='store_true')


    parser.add_argument('--notification_type')
    parser.add_argument('--service')
    parser.add_argument('--host')
    parser.add_argument('--address')
    parser.add_argument('--state')
    parser.add_argument('--date_time')
    parser.add_argument('--additional_info')
    parser.add_argument('--service_alert')
    parser.add_argument('--contact_mail')

    args = parser.parse_args()

    nagios_data = {
        'notification_type': args.notification_type,
        'service':  args.service,
        'host': args.host,
        'address': args.address,
        'state': args.state,
        'date_time': args.date_time,
        'additional_info': args.additional_info,
        'service_alert': args.service_alert,
        'contact_mail': args.contact_mail
    }



    with open(args.config_file) as fp:
        config = yaml.load(fp)

    sfdc_oauth2 = OAuth2(client_id=config['sfdc_client_id'],
                         client_secret=config['sfdc_client_secret'],
                         username=config['sfdc_username'],
                         password=config['sfdc_password'],
                         auth_url=config['sfdc_auth_url'])


    sfdc_client = Client(sfdc_oauth2)



    data = {
        'Payload__c':  json.dumps(nagios_data)
        }



#    sfdc_client.create_ticket(data)
    sfdc_client.create_mos_alert(data)


# Serach example
#    a=sfdc_client.search("SELECT Id from Case")
#    for b  in a:
#        print(b['Id'])
#        sfdc_client.get_case(b['Id'])
#

if __name__ == '__main__':
    main()


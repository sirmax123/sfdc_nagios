#  Plugin for nagios  to notify to  SalesForce

This is POC.
Just for tests.

Designet to use MOS_Alert object, always creates new object.


## How to install and configure

Installation:

1. mkdir /usr/lib/nagios/plugins/sfdc/
2. cp salesforce.py sfdc_nagios.py sfdc_nagios.yaml /usr/lib/nagios/plugins/sfdc/
3. copy to nagios config dir or add to nagios file command definition from sfdc.cfg file. E.g. cp sfdc.cfg /etc/nagios3/conf.d/
4. Configure notification for group/user. E.g. service_notification_commands  notify-sfdc-mos-alert
5. Restart nagios


## Config file parameters

*  sfdc_client_id: Client ID of SFDC application
*  sfdc_client_secret: Client secret of SFDC application
*  sfdc_username: User Name
*  sfdc_password: User Password
*  sfdc_auth_url: Auth URL, looks like 'https://someurl.my.salesforce.com/'
*  environment: OpenStack env ID.
*  sfdc_organization_id: SFDC Organization ID.

sfdc_organization_id is used only for customer's accounts because in general username may by not global-unique. 
So this paraneter is 'domain of visability' for username and must be configured *ONLY* for custome's account.






#  Plugin for nagios  to notify to  SalesForce

This is POC.
Just for tests.

Designet to use MOS_Alert object, always creates new object.


## How to install and configure

Installation:

1. mkdir /usr/lib/nagios/plugins/sfdc/
2. cp salesforce.py sfdc_nagios.py sfdc_nagios.yaml /usr/lib/nagios/plugins/sfdc/
3. copy to nagios config dir or add to nagios file command definition from notify-sfdc-mos-alert.cfg file. E.g. cp notify-sfdc-mos-alert.cfg /etc/nagios3/conf.d/
4. Configure notification for group/user. E.g. service_notification_commands  notify-sfdc-mos-alert
5. Restart nagios



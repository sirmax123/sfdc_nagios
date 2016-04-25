import requests
import json


requests.packages.urllib3.disable_warnings()

class OAuth2(object):
    def __init__(self, client_id, client_secret, username, password, auth_url=None):
        if not auth_url:
            auth_url = 'https://login.salesforce.com'

        self.auth_url = auth_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password

    def authenticate(self):
        data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password,
        }

        url = '{}/services/oauth2/token'.format(self.auth_url)
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()


class Client(object):
    def __init__(self, oauth2):
        self.oauth2 = oauth2

        self.access_token = None
        self.instance_url = None

    def ticket(self, id):
        try:
            return self.get('/services/data/v36.0/sobjects/proxyTicket__c/{}'.format(id)).json()
        except requests.HTTPError:
            return False

    def create_mos_alert(self, data):
        return self.post('/services/data/v36.0/sobjects/MOS_Alerts__c', json=data)

    def create_mos_alert_comment(self, data):
        return self.post('/services/data/v36.0/sobjects/MOS_Alert_Comment__c', json=data)


    def create_case(self, data):
        return self.post('/services/data/v36.0/sobjects/Case', json=data).json()


    def create_ticket(self, data):
        return self.post('/services/data/v36.0/sobjects/Case', json=data).json()

    def get_case(self, id):
        return self.get('/services/data/v36.0/sobjects/Case/{}'.format(id))

    def get_mos_alert(self, id):
        return self.get('/services/data/v36.0/sobjects/MOS_Alerts__c/{}'.format(id))

    def update_ticket(self, id, data):
        return self.patch('/services/data/v36.0/sobjects/proxyTicket__c/{}'.format(id), json=data)

    def update_mos_alert(self, id, data):
        return self.patch('/services/data/v36.0/sobjects/MOS_Alerts__c/{}'.format(id), json=data)


    def update_comment(self, id, data):
        return self.patch('/services/data/v36.0/sobjects/proxyTicketComment__c/{}'.format(id), json=data)

    def create_ticket_comment(self, data):
        return self.post('/services/data/v36.0/sobjects/proxyTicketComment__c', json=data).json()

    def environment(self, id):
        return self.get('/services/data/v36.0/sobjects/Environment__c/{}'.format(id)).json()

    def ticket_comments(self, ticket_id):
        return self.search("SELECT Comment__c, CreatedById, external_id__c, Id, CreatedDate, createdby.name "
                           "FROM proxyTicketComment__c "
                           "WHERE related_id__c='{}'".format(ticket_id))

    def ticket_comment(self, comment_id):
        return self.get('/services/data/v36.0/query',
                        params=dict(q="SELECT Comment__c, CreatedById, Id "
                                      "FROM proxyTicketComment__c "
                                      "WHERE external_id__c='{}'".format(comment_id))).json()
    def test(self):
        print("test")

    def search(self, query):
        response = self.get('/services/data/v36.0/query', params=dict(q=query)).json()
        while True:
            for record in response['records']:
                yield record

            if response['done']:
                return

            response = self.get(response['nextRecordsUrl']).json()

    def get(self, url, **kwargs):
        return self._request('get', url, **kwargs)

    def patch(self, url, **kwargs):
        return self._request('patch', url, **kwargs)

    def post(self, url, **kwargs):
        return self._request('post', url, **kwargs)

    def _request(self, method, url, headers=None, **kwargs):
        if not headers:
            headers = {}

        if not self.access_token or not self.instance_url:
            result = self.oauth2.authenticate()

            self.access_token = result['access_token']
            self.instance_url = result['instance_url']

        headers['Authorization'] = 'Bearer {}'.format(self.access_token)

        url = self.instance_url + url

        response = requests.request(method, url, headers=headers, **kwargs)

# Debug only
#        print(response.status_code)
#        try:
#          print(json.dumps(response.json(),sort_keys=True, indent=4, separators=(',', ': ') ) )
#        except Exception:
#           print(response.content)
#        response.raise_for_status()

        return response

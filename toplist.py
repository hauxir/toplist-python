#!/usr/bin/python
import requests
import json
import jwt

TOPLIST_API = "https://api.thetoplistapp.com/v1"

"""
LOGIN URL:
https://www.facebook.com/v2.8/dialog/oauth?redirect_uri=fb1832655376972820%3A%2F%2Fauthorize%2F&state=%7B%22challenge%22%3A%22TmhoovL4TZtEJduJuxfewrMtUlU%253D%22%2C%220_auth_logger_id%22%3A%22AA6B61AD-EBBC-4C52-BAA7-1D577C6C4BB7%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=public_profile%2Cemail&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=1832655376972820&ret=login&sdk=ios&fbapp_pres=1&logger_id=AA6B61AD-EBBC-4C52-BAA7-1D577C6C4BB7&ext=1494637564&hash=AeYAq8B7CAB7h3SZ


LOOK AT THE RESPONSE IN VERIFY TO FIND THE FACEBOOK TOKEN
"""

class AuthException(Exception):
    pass

class TopListAPI:

    def login(self, fbtoken):
        response = requests.post(
            "https://api.thetoplistapp.com/v1/login",
            json={'accessToken': fbtoken}
        )
        content = response.content
        try:
            self.token = json.loads(response.content)['token']
	    self.user_id = jwt.decode(
                self.token,
                'secret',
                algorithms=['HS256'],
                options={'verify_signature': False}
            )['userID']
            print "LOGGED IN!"
        except ValueError:
            self.token = None
            raise AuthException(content)

    def _get(self, path):
        if not self.token:
            raise Exception("You need to log in")
        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        response = requests.get(TOPLIST_API + path, headers=headers)
        content = response.value
        try:
            return json.loads(content)
        except ValueError:
            print content

    def _post(self, path, data):
        if not self.token:
            raise Exception("You need to log in")
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        response = requests.post(
                TOPLIST_API + path,
                headers=headers, json=data
        )
        content = response.content
        try:
            return json.loads(content)
        except ValueError:
            print content

    def _collect_dollars(self, ndollars):
        response = self._post('/collect', {
            "productID": "top_dollar_" + str(ndollars),
            "filters": {
                "filters": [],
                "dateFilter": False
            }
        })
        print "Collected " + str(ndollars) + " dollars"
        return response

    def _set_quote(self, user_id, quote):
        return self._post('/user/' + user_id + '/quote', {
            'quote': quote
        })

    def _get_orders(self, user_id):
        return self._get('/orders/' + user_id)

    def get_filters(self):
        return self._get('/filters')

    def get_entry(self, eid):
        return self._get('/entry/' + str(eid))

    def get_order(self, oid):
        return self._get('/order/' + str(oid))

    def registerpush(self, rid):
        return self._get('/registerPush', {'registrationID': rid})

    def collect_1_dollar(self):
        return self._collect_dollars(1)

    def collect_5_dollars(self):
        return self._collect_dollars(5)

    def collect_10_dollars(self):
        return self._collect_dollars(10)

    def collect_30_dollars(self):
        return self._collect_dollars(30)

    def collect_60_dollars(self):
        return self._collect_dollars(60)

    def set_quote(self, quote):
        return self._set_quote(self.user_id, quote)

    def get_orders(self):
        return self._get_orders(self.user_id)

    def list(self):
        return self._get('/list')

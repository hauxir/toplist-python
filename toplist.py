#!/usr/bin/python
import requests
import json
import jwt

TOPLIST_API = 'https://api.thetoplistapp.com/v1'

"""
LOGIN URL:
https://www.facebook.com/v2.8/dialog/oauth?redirect_uri=fb1832655376972820%3A%2F%2Fauthorize%2F&state=%7B%22challenge%22%3A%22TmhoovL4TZtEJduJuxfewrMtUlU%253D%22%2C%220_auth_logger_id%22%3A%22AA6B61AD-EBBC-4C52-BAA7-1D577C6C4BB7%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C%223_method%22%3A%22sfvc_auth%22%7D&scope=public_profile%2Cemail&response_type=token%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id=1832655376972820&ret=login&sdk=ios&fbapp_pres=1&logger_id=AA6B61AD-EBBC-4C52-BAA7-1D577C6C4BB7&ext=1494637564&hash=AeYAq8B7CAB7h3SZ


LOOK AT THE RESPONSE IN VERIFY TO FIND THE FACEBOOK TOKEN
"""

class TopListException(Exception):
    pass

class TopListAPI(object):

    def _request(self, path, reqfun, data=None):
        if not self.token:
            raise TopListException('You need to log in')
        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        response = reqfun(
                TOPLIST_API + path,
                headers=headers, json=data
        )
        content = response.content
        try:
            return json.loads(content)
        except ValueError:
            raise TopListException(content)

    def _get(self, path):
        return self._request(path, requests.get)

    def _put(self, path, data):
        return self._request(path, requests.put, data=data)

    def _post(self, path, data):
        return self._request(path, requests.post, data=data)

    def _collect_dollars(self, ndollars, filters=[], dateFilter=False):
        return self._post('/collect', {
            'productID': 'top_dollar_' + str(ndollars),
            'filters': {
                'filters': filters,
                'dateFilter': dateFilter
            }
        })

    def _set_quote(self, user_id, quote):
        return self._put('/user/' + str(user_id) + '/quote', {
            'quote': quote
        })

    def _get_orders(self, user_id):
        return self._get('/orders/' + str(user_id))

    def login(self, fbtoken):
        response = requests.post(
            TOPLIST_API + '/login',
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
        except ValueError:
            raise TopListException(content)

    def get_filters(self):
        return self._get('/filters')

    def get_entry(self, eid):
        return self._get('/entry/' + str(eid))

    def get_orders(self):
        return self._get_orders(self.user_id)

    def get_order(self, oid):
        return self._get('/order/' + str(oid))

    def registerpush(self, rid):
        return self._post('/registerPush', {'registrationID': rid})

    def collect_1_dollar(self, filters=[], dateFilter=False):
        return self._collect_dollars(1, filters, dateFilter)

    def collect_5_dollars(self, filters=[], dateFilter=False):
        return self._collect_dollars(5, filters, dateFilter)

    def collect_10_dollars(self, filters=[], dateFilter=False):
        return self._collect_dollars(10, filters, dateFilter)

    def collect_30_dollars(self, filters=[], dateFilter=False):
        return self._collect_dollars(30, filters, dateFilter)

    def collect_60_dollars(self, filters=[], dateFilter=False):
        return self._collect_dollars(60, filters, dateFilter)

    def set_quote(self, quote):
        return self._set_quote(self.user_id, quote)

    def get_list(self):
        return self._get('/list')

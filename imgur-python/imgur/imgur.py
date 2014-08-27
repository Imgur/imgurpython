#!/usr/bin/env python3

import json
from .auth.expired import Expired

try:
    from urllib.request import urlopen as urllibopen
    from urllib.request import HTTPError
except ImportError:
    from urllib2 import urlopen as urllibopen
    from urllib2 import HTTPError


class Imgur:
    def __init__(self, client_id, secret, auth, rate_limit):
        self.client_id = client_id
        self.secret = secret
        self.auth = auth
        self.rate_limit = rate_limit

    def get_rate_limit(self):
        return self.rate_limit

    def get_auth(self):
        return self.auth

    def get_client_id(self):
        return self.client_id

    def retrieve_raw(self, request):
        request = self.auth.add_authorization_header(request)
        req = urllibopen(request)
        res = json.loads(req.read().decode('utf-8'))

        return req, res

    def retrieve(self, request):
        try:
            (req, res) = self.retrieve_raw(request)
        except HTTPError as e:
            if e.code == 403:
                raise Expired()
            else:
                print("Error %d\n%s\n" % (e.code, e.read()))
                raise e

        self.rate_limit.update(req.info())
        if res['success'] is not True:
            raise Exception(res['data']['error']['message'])

        return res['data']
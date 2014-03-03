#!/usr/bin/env python3

import json

try:
    from urllib.request import urlopen as UrlLibOpen
    from urllib.request import HTTPError
except ImportError:
    from urllib2 import urlopen as UrlLibOpen
    from urllib2 import HTTPError

from .Auth.Expired import Expired

class Imgur:
    
    def __init__(self, client_id, secret, auth, ratelimit):
        self.client_id = client_id
        self.secret = secret
        self.auth = auth
        self.ratelimit = ratelimit

    def retrieve_raw(self, request):
        request = self.auth.add_authorization_header(request)
        req = UrlLibOpen(request)
        res = json.loads(req.read().decode('utf-8'))
        return (req, res)

    def retrieve(self, request):
        try:
            (req, res) = self.retrieve_raw(request)
        except HTTPError as e:
            if e.code == 403:
                raise Expired()
            else:
                print("Error %d\n%s\n" % (e.code, e.read()))
                raise e

        self.ratelimit.update(req.info())
        if res['success'] is not True:
            raise Exception(res['data']['error']['message'])

        return res['data']

    def get_rate_limit(self):
        return self.ratelimit

    def get_auth(self):
        return self.auth
    
    def get_client_id(self):
        return self.client_id

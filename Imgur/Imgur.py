#!/usr/bin/env python3

import json
try:
    import urllib.request
    from urllib.request import HTTPError
except:
    import urllib2 as urllib
    from urllib2 import HTTPError
from .Auth.Expired import Expired

class Imgur:
    
    def __init__(self, client_id, secret, auth, ratelimit):
        self.client_id = client_id
        self.secret = secret
        self.auth = auth
        self.ratelimit = ratelimit

    def retrieveRaw(self, request):
        request = self.auth.addAuthorizationHeader(request)
        try:
            req = urllib.request.urlopen(request)
        except:
            req = urllib.urlopen(request)
        res = json.loads(req.read().decode('utf-8'))
        return (req, res)

    def retrieve(self, request):

        try:
            (req, res) = self.retrieveRaw(request)
        except HTTPError as e:
            raise
            if e.code == 403:
                raise Expired()
            else:
                print("Error %d\n%s\n" % (e.code, e.read()))
                raise e

        self.ratelimit.update(req.info())
        if res['success'] is not True:
            raise Exception(res['data']['error']['message'])

        return res['data']

    def getRateLimit(self):
        return self.ratelimit

    def getAuth(self):
        return self.auth
    
    def getClientID(self):
        return self.client_id

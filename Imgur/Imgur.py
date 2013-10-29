#!/usr/bin/env python3

import urllib.request, json

class Imgur:
    
    def __init__(self, client_id, secret, auth, ratelimit):
        self.client_id = client_id
        self.secret = secret
        self.auth = auth
        self.ratelimit = ratelimit

    def retrieveRaw(self, request):
        request = self.auth.addAuthorizationHeader(request)
        req = urllib.request.urlopen(request)
        res = json.loads(req.read().decode('utf-8'))
        return (req, res)

    def retrieve(self, request):
        (req, res) = self.retrieveRaw(request)
        self.ratelimit.update(req.info())
        if res['success'] is not True:
            raise Exception(res['error'])

        return res['data']

    def getRateLimit(self):
        return self.ratelimit

    def getAuth(self):
        return self.auth
    
    def getClientID(self):
        return self.client_id

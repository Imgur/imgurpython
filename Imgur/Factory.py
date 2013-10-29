#!/usr/bin/env python3

import urllib.request, urllib.parse, base64, os.path
from . import Imgur, RateLimit
from .Auth import Authorization, Anonymous

class Factory:

    API_URL = "https://api.imgur.com/3/"

    def __init__(self, config):
        self.config = config

    def buildAPI(self, auth = None, ratelimit = None):
        if auth is None:
            auth = self.buildAuth('anonymous')
        if ratelimit is None:
            ratelimit = self.buildRateLimit()
        return Imgur.Imgur(self.config['client_id'], self.config['secret'], auth, ratelimit)

    def buildAuth(self, kind):
        '''Build an instance of Imgur.Auth
        
        kind: 'authorization'   OAuth2 authorization code
              None              Anonymous
        '''
        if kind == 'authorization':
            return Authorization.Authorization(self.config['client_id'], self.config['secret'])
        if kind is None or kind == 'anonymous':
            return Anonymous.Anonymous(self.config['client_id'])

    def buildRequest(self, endpoint, data = None):
        '''Expects an endpoint like 'image' or a tuple like ('gallery', 'hot', 'viral', '0')'''
        if isinstance(endpoint, str):
            url = self.API_URL + endpoint + '.json'
        else:
            url = self.API_URL + '/'.join(endpoint) + ".json"

        req = urllib.request.Request(url)
        if data is not None:
            req.add_data(urllib.parse.urlencode(data).encode('utf-8'))
        return req
    
    def buildRateLimit(self, limits = None):
        '''If none, defaults to fresh rate limits. Else expects keys "client_limit", "user_limit", "user_reset"'''
        if limits is not None:
            return RateLimit.RateLimit(limits['client_limit'], limits['user_limit'], limits['user_reset'])
        else:
            return RateLimit.RateLimit()
    
    def buildRequestUploadFromPath(self, path, params = dict()):
        fd = open(path, 'rb')
        contents = fd.read()
        b64 = base64.b64encode(contents)
        data = {
            'image': b64,
            'type': 'base64',
            'name': os.path.basename(path)
        }
        data.update(params)
        return self.buildRequest('upload', data)
        

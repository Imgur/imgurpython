#!/usr/bin/env python3

import urllib.request, urllib.parse
from . import Imgur, RateLimit
from .Auth import Authorization, Anonymous

class Factory:

    API_URL = "https://api.imgur.com/3/"

    def __init__(self, config):
        self.config = config

    def buildAPI(self, auth):
        return Imgur.Imgur(self.config['client_id'], self.config['secret'], auth)

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
        url = self.API_URL + '/'.join(endpoint) + ".json"
        req = urllib.request.Request(url)
        if data is not None:
            req.add_data(urllib.parse.urlencode(data))
        return req
    
    def buildRateLimit(self, limits = None):
        if limits is not None:
            return RateLimit.RateLimit(limits['client_limit'], limits['user_limit'], limits['user_reset'])
        else:
            return RateLimit.RateLimit()


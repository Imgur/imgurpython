#!/usr/bin/env python3

import urllib.request, urllib.parse, base64, os.path
from .Imgur import Imgur
from .RateLimit import RateLimit
from .Auth.AccessToken import AccessToken
from .Auth.Anonymous import Anonymous

class Factory:

    API_URL = "https://api.imgur.com/"

    def __init__(self, config):
        self.config = config
        if 'api' in self.config:
            self.API_URL = self.config['api']

    def getAPIUrl(self):
        return self.API_URL

    def buildAPI(self, auth = None, ratelimit = None):
        if auth is None:
            auth = self.buildAnonymousAuth()
        if ratelimit is None:
            ratelimit = self.buildRateLimit()
        return Imgur(self.config['client_id'], self.config['secret'], auth, ratelimit)

    def buildAnonymousAuth(self):
        return Anonymous(self.config['client_id'])

    def buildOAuth(self, access, refresh, expire_time):
        return AccessToken(access, refresh, expire_time)

    def buildRequest(self, endpoint, data = None):
        '''Expects an endpoint like 'image.json' or a tuple like ('gallery', 'hot', 'viral', '0'). 
        
        Prepends 3/ and appends \.json to the tuple-form, not the endpoint form.'''
        if isinstance(endpoint, str):
            url = self.API_URL + endpoint
        else:
            url = self.API_URL + '3/' + ('/'.join(endpoint)) + ".json"

        req = urllib.request.Request(url)
        if data is not None:
            req.add_data(urllib.parse.urlencode(data).encode('utf-8'))
        return req
    
    def buildRateLimit(self, limits = None):
        '''If none, defaults to fresh rate limits. Else expects keys "client_limit", "user_limit", "user_reset"'''
        if limits is not None:
            return RateLimit(limits['client_limit'], limits['user_limit'], limits['user_reset'])
        else:
            return RateLimit()

    def buildRateLimitsFromServer(self, api):
        '''Get the rate limits for this application and build a rate limit model from it.'''
        req = self.buildRequest('credits')
        res = api.retrieve(req)
        return RateLimit(res['ClientRemaining'], res['UserRemaining'], res['UserReset'])

    
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
        return self.buildRequest(('upload',), data)

    def buildRequestOAuthTokenSwap(self, grant_type, token):
        data = {
            'client_id': self.config['client_id'],
            'client_secret': self.config['secret'],
            'grant_type': grant_type
        }

        if grant_type == 'authorization_code':
            data['code'] = token
        if grant_type == 'pin':
            data['pin'] = token

        return self.buildRequest('oauth2/token', data)

    def buildRequestOAuthRefresh(self, refresh_token):
        data = {
            'refresh_token': refresh_token,
            'client_id': self.config['client_id'],
            'client_secret': self.config['secret'],
            'grant_type': 'refresh_token'
        }
        return self.buildRequest('oauth2/token', data)

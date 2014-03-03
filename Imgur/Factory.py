#!/usr/bin/env python3

import base64, os.path, time as dt

try:
    from urllib.request import Request as UrlLibRequest
    from urllib.parse import urlencode as UrlLibEncode
except ImportError:
    from urllib2 import Request as UrlLibRequest
    from urllib import urlencode as UrlLibEncode
    
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

    def get_api_url(self):
        return self.API_URL

    def build_api(self, auth = None, ratelimit = None):
        if auth is None:
            auth = self.build_anonymous_auth()
        if ratelimit is None:
            ratelimit = self.build_rate_limit()
        return Imgur(self.config['client_id'], self.config['secret'], auth, ratelimit)

    def build_anonymous_auth(self):
        return Anonymous(self.config['client_id'])

    def build_oauth(self, access, refresh, expire_time = None):
        now = int(dt.time())
        if expire_time is None:
            return AccessToken(access, refresh, now)
        else:
            return AccessToken(access, refresh, expire_time)

    def build_request(self, endpoint, data = None):
        '''Expects an endpoint like 'image.json' or a tuple like ('gallery', 'hot', 'viral', '0'). 
        
        Prepends 3/ and appends \.json to the tuple-form, not the endpoint form.'''
        if isinstance(endpoint, str):
            url = self.API_URL + endpoint
        else:
            url = self.API_URL + '3/' + ('/'.join(endpoint)) + ".json"

        req = UrlLibRequest(url)
        if data is not None:
            req.add_data(UrlLibEncode(data).encode('utf-8'))
        return req
    
    def build_rate_limit(self, limits = None):
        '''If none, defaults to fresh rate limits. Else expects keys "client_limit", "user_limit", "user_reset"'''
        if limits is not None:
            return RateLimit(limits['client_limit'], limits['user_limit'], limits['user_reset'])
        else:
            return RateLimit()

    def build_rate_limits_from_server(self, api):
        '''Get the rate limits for this application and build a rate limit model from it.'''
        req = self.build_request('credits')
        res = api.retrieve(req)
        return RateLimit(res['ClientRemaining'], res['UserRemaining'], res['UserReset'])

    
    def build_request_upload_from_path(self, path, params = dict()):
        fd = open(path, 'rb')
        contents = fd.read()
        b64 = base64.b64encode(contents)
        data = {
            'image': b64,
            'type': 'base64',
            'name': os.path.basename(path)
        }
        data.update(params)
        return self.build_request(('upload',), data)

    def build_request_oauth_token_swap(self, grant_type, token):
        data = {
            'client_id': self.config['client_id'],
            'client_secret': self.config['secret'],
            'grant_type': grant_type
        }

        if grant_type == 'authorization_code':
            data['code'] = token
        if grant_type == 'pin':
            data['pin'] = token

        return self.build_request('oauth2/token', data)

    def build_request_oauth_refresh(self, refresh_token):
        data = {
            'refresh_token': refresh_token,
            'client_id': self.config['client_id'],
            'client_secret': self.config['secret'],
            'grant_type': 'refresh_token'
        }
        return self.build_request('oauth2/token', data)

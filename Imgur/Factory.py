#!/usr/bin/env python3

import Imgur, Imgur.Auth.Anonymous, Imgur.Auth.Authorization

class Factory:
    def __init__(self, config):
        self.config = config

    def buildAPI(self, auth):
        return Imgur(self.config['client_id'], self.config['secret'], auth)

    def buildAuth(self, kind):
        '''Build an instance of Imgur.Auth
        
        kind: 'authorization'   OAuth2 authorization code
              None              Anonymous
        '''
        if kind == 'authorization':
            return Imgur.Auth.Authorization(self.config['client_id'], self.config['secret'])
        if kind is None:
            return Imgur.Auth.Anonymous(self.config['client_id'])

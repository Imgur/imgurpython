#!/usr/bin/env python3

class Base:
    def need_to_authorize(self, time):
        '''Do we need to refresh our authorization token?'''
        pass
    def authorize(self, api, requestfactory):
        '''Refresh our access token'''
        pass
    def add_authorization_header(self, request):
        pass
        

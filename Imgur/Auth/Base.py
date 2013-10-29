#!/usr/bin/env python3

class Base:
    def needToAuthorize(self, time):
        '''Do we need to refresh our authorization token?'''
        pass
    def authorize(self, api, requestfactory):
        '''Refresh our access token'''
        pass
    def addAuthorizationHeader(self, request):
        pass
        

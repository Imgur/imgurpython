#!/usr/bin/env python3

from .Base import Base as AuthBase
import time as dt

class AccessToken(AuthBase):
    def __init__(self,  access, refresh, expire_time):
        self.access = access
        self.refresh = refresh
        self.expire_time = expire_time

    def needToAuthorize(self, time):
        return (self.expire_time <= time)

    def addAuthorizationHeader(self, request):
        request.add_header('Authorization', 'Bearer ' + self.access)
        return request

    def getAccessToken(self):
        return self.access

    def getRefreshToken(self):
        return self.refresh

#!/usr/bin/env python3

from .base import Base as AuthBase


class AccessToken(AuthBase):
    def __init__(self,  access, refresh, expire_time):
        self.access = access
        self.refresh = refresh
        self.expire_time = expire_time

    def need_to_authorize(self, time):
        return self.expire_time <= time

    def add_authorization_header(self, request):
        request.add_header('Authorization', 'Bearer %s' % self.access)
        return request

    def get_access_token(self):
        return self.access

    def get_refresh_token(self):
        return self.refresh

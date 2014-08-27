#!/usr/bin/env python3

from .base import Base as AuthBase


class Anonymous(AuthBase):
    def __init__(self, client_id):
        self.client_id = client_id

    def need_to_authorize(self, time):
        return False

    def authorize(self, api, request_factory):
        pass

    def add_authorization_header(self, request):
        request.add_header('Authorization', 'Client-ID %s' % self.client_id)
        return request
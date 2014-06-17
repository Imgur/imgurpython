#!/usr/bin/env python3

class anonymous:
    def __init__(self, client_id):
        self.client_id = client_id

    def need_to_authorize(self):
        return False

    def authorize(self):
        pass

    def add_authorization_header(self, request):
        request.add_header('Authorization', 'Client-ID ' + self.client_id)
        return request

#!/usr/bin/env python3

class Anonymous:
    def __init__(self, client_id):
        self.client_id = client_id

    def needToAuthorize(self):
        return False

    def authorize(self):
        pass

    def addAuthorizationHeader(self, request):
        request.add_header('Authorization', 'Client-ID ' + self.client_id)
        return request

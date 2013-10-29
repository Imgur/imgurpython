#!/usr/bin/env pythone

class Authorization:
    def __init__(self, client_id, secret, token):
        self.client_id = client_id
        self.secret = secret
        self.authorization_token = token

    def addAuthorizationHeader(self, request):
        request.add_header('Authorization', 'Bearer ' + self.authorization_token)
        return request

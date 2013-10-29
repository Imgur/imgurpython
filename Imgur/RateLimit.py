#!/usr/bin/env python3

import time as dt

class RateLimit:

    def __init__(self, client_remaining = 12500, user_remaining = 500, user_reset = None):
        self.client_remaining = client_remaining
        self.user_remaining = user_remaining
        self.user_reset = user_reset

    def update(self, headers):
        '''Update the rate limit state with a fresh API response'''

        self.client_remaining = headers['X-RateLimit-ClientRemaining']
        self.user_remaining = headers['X-RateLimit-UserRemaining']
        self.user_reset = headers['X-RateLimit-UserReset']
        
    def is_over(self, time = None):
        return self.would_be_over(0, time)
        
    def would_be_over(self, cost, time = None):
        if time is None:
            time = dt.time()

        return self.client_remaining < cost or (self.user_reset is not None and self.user_reset > time and self.user_remaining < cost)

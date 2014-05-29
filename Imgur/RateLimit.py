#!/usr/bin/env python3

import time as dt

class RateLimit:

    def __init__(self, client_remaining = 12500, user_remaining = 500, user_reset = None):
        self.client_remaining = client_remaining
        self.user_remaining = user_remaining
        self.user_reset = user_reset

    def update(self, headers):
        '''Update the rate limit state with a fresh API response'''

        if 'X-RateLimit-ClientRemaining' in headers:
            self.client_remaining = int(headers['X-RateLimit-ClientRemaining'])
            self.user_remaining = int(headers['X-RateLimit-UserRemaining'])
            self.user_reset = int(headers['X-RateLimit-UserReset'])
        
    def is_over(self, time):
        return self.would_be_over(0, time)
        
    def would_be_over(self, cost, time):
        return self.client_remaining < cost or (self.user_reset is not None and self.user_reset > time and self.user_remaining < cost)

    def __str__(self, time = None):
        # can't ask for time by DI when doing str(x).
        if time is None:
            time = dt.time()

        exp = int(self.user_reset) - int(time)
        return "<RateLimits: %d for client, %d for user, %d seconds until reset>" % (self.client_remaining, self.user_remaining, exp)

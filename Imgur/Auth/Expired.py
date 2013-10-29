#!/usr/bin/env python3

class Expired(BaseException):
    def __str__(self):
        return "Access token invalid or expired."


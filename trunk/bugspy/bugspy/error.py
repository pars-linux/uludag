#!/usr/bin/python
# -*- coding: utf-8 -*-

class BugzillaError(Exception):
    '''Generic error class'''
    pass

class LoginError(BugzillaError):
    '''Error in login page'''
    def __init__(self, msg):
        self.msg = msg

class ParseError(BugzillaError):
    '''Parse error.'''
    def __init__(self, msg):
        self.msg = msg

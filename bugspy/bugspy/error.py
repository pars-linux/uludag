#!/usr/bin/python
# -*- coding: utf-8 -*-

class BugzillaError(Exception):
    '''Generic error class'''
    def __init__(self, msg):
        self.msg = msg

class LoginError(BugzillaError):
    pass

class ParseError(BugzillaError):
    pass

class ModifyError(BugzillaError):
    def __init__(self, msg, response):
        self.msg = msg
        self.response = response

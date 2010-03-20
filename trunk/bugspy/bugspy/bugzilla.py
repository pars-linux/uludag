#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Bugzilla tool for Pardus. I'm really bored with other distro's tools.
#
# Eren Türkay <eren:pardus.org.tr> // 21 March, 2010
#

from mechanize import Browser
import logging

logging.basicConfig()
logging.getLogger("bugzilla")

# FIXME: Read username and password from this file which is INI format.
CONFIG_FILE = '~/.bugspy.conf'
BUGZILLA_URL = 'http://bugs.pardus.org.tr/'
USERNAME = 'eren@pardus.org.tr'
PASSWORD = 'Password'

class BugzillaError(Exception):
    '''Generic error class'''
    pass

class LoginError(BugzillaError):
    '''Error in login page'''
    def __init__(self, msg):
        self.msg = msg

class Bugzilla:
    def __init__(self, bugzilla_url, username=None, password=None):
        self.bugzilla_url = bugzilla_url
        self.username = username
        self.password = password

        logging.debug("Using username: %s && password: %s" % (username, password))

        self.browser = Browser()
        self.browser.open(bugzilla_url)

    def login(self):
        if not self.username or not self.password:
            logging.debug("login: User or Password is not supplied. Exiting..")
            raise LoginError("User or Password is not supplied")

def main():
    bugzilla = Bugzilla(BUGZILLA_URL)
    bugzilla.login()

if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Bugzilla tool for Pardus. I'm really bored with other distro's tools.
#
# Eren Türkay <eren:pardus.org.tr> // 21 March, 2010
#

from mechanize import Browser
import logging

from bugspy.error import LoginError

logging.basicConfig()
log = logging.getLogger("bugzilla")
log.setLevel(logging.DEBUG)

# FIXME: Read username and password from this file which is INI format.
CONFIG_FILE = '~/.bugspy.conf'
BUGZILLA_URL = 'http://bugs.pardus.org.tr/'
USERNAME = 'eren@pardus.org.tr'
PASSWORD = 'Password'

class Bugzilla:
    """
    Main Bugzilla class that does all the thing, getting bugs, closing, commenting etc..

    Attributes:
        bugzilla_url: Bugzilla url to open
        username: Username to use. Ie. eren@pardus.org.tr
        password: Bugzilla password.
        browser: Browser object from mechanize library
    """

    def __init__(self, bugzilla_url, username=None, password=None):
        """Initalises bugzilla_url, username and password variables and opens bugzilla page.

        Args:
            bugzilla_url: Bugzilla url to open
            username: Username to use. Ie. eren@pardus.org.tr
            password: Bugzilla password.
        """

        log.debug("Bugzilla class initialised")

        self.bugzilla_url = bugzilla_url
        self.username = username
        self.password = password

        self.browser = Browser()
        self.browser.open(bugzilla_url)

        # if username and password is supplied, it means we are expected to login.
        self.is_auth_needed = bool(username and password)

    def login(self):
        """Logins to bugzilla

        Raises:
            AuthError: User or Password is wrong.
        """
        if self.is_auth_needed:
            log.info("Trying to login...")
            print "Do login stuff here"


def main():
    bugzilla = Bugzilla(BUGZILLA_URL)
    bugzilla.login()

if __name__ == '__main__':
    main()

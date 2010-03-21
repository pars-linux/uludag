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
from bugspy.constants import Constants
from bugspy.config import Config

logging.basicConfig()
log = logging.getLogger("bugzilla")
log.setLevel(logging.DEBUG)

class Bugzilla:
    """
    Main Bugzilla class that does all the thing, getting bugs, closing, commenting etc..

    If username ans password is supplied, it will try to login and save cookies for the future uses. For read-only operations (gettings bugs, etc.), login is not needed

    NOTE: Please do not write the last / on bugzilla_url. It is used to determine full path and it is required to supply it without last /.

    Attributes:
        bugzilla_url: Bugzilla url to open. Ie: http://bugs.pardus.org.tr
        username: Username to use. Ie: eren@pardus.org.tr
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

        # define constants class so that we do not mess up the code with lots of "self.bugzilla_url + "/show_bug.cgi?id=123456".
        self.constants = Constants(bugzilla_url)

        self.bugzilla_url = bugzilla_url
        self.username = username
        self.password = password

        self.browser = Browser()
        # disable robots txt. Pardus.org.tr has it and we cannot open any page if it is enabled. Also, kim takar yalova kaymakamını? :)
        self.browser.set_handle_robots(False)
        self.browser.open(bugzilla_url)

        # if username and password is supplied, it means we are expected to login.
        self.is_auth_needed = bool(username and password)

    def login(self):
        """Logins to bugzilla

        Returns:
            True if login is successfull. Raises exception when it fails

        Raises:
            LoginError: User or Password is wrong.
        """
        if self.is_auth_needed:
            log.info("Trying to login...")

            # Bugzilla page does not provide form name for it. Select it by offset
            log.debug("Selecting 5th form")
            self.browser.select_form(nr=5)
            self.browser["Bugzilla_login"] = self.username
            self.browser["Bugzilla_password"] = self.password
            log.debug("Submitting the form")
            response = self.browser.submit()
            log.debug("Getting the response")
            response = response.read()

            if response.find(self.constants.LOGIN_FAILED_STRING) > -1:
                # DAMN! We found the string and failed to login..
                raise LoginError("User or Password is invalid")
            else:
                return True

        def get_bug(self, bug_id):
            """Gets information about but

            Args:
                bug_id: Bug id to get

            Returns:
                # FIXME: Class representation of a bug?
            """

            

    # FIXME: remove it on production
    def get_dummy_bug(self):
        log.debug("Calling dummy bug")
        print self.constants.get_bug_show_page(12146)
        self.write_tmp(self.browser.open(self.constants.get_bug_show_page(12146)).read())

    # FIXME: remove it on production
    def write_tmp(self, data):
        open("/tmp/bug.html", "w+").write(data)

def main():
    c = Config()

    bugzilla = Bugzilla(c.bugzillaurl, c.username, c.password)
    bugzilla.login()
    bugzilla.get_dummy_bug()

if __name__ == '__main__':
    main()

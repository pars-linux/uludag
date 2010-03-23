#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib

class Constants:
    """Class that defines constants, both static and dynamic.

    It also automatically generates url for pages according to bugzilla_url variable so that code would be cleaner.

    Attributes:
        LOGIN_FAILED_STRING: The string to check whether we logged in or not
        SHOW_BUG_URL: Cgi script address for showing bugs
        VERSION: Version of the package
        USER_AGENT: User-agent header to send

    """
    VERSION = "0.1"

    LOGIN_FAILED_STRING = "Invalid Username Or Password"
    NO_PERMISSON_STRING = "You are not authorized to access bug"
    BUG_PROCESS_OK_STRING = "Changes submitted for"

    SHOW_BUG_URL = "show_bug.cgi"
    ENTER_BUG_URL = "enter_bug.cgi"
    USER_AGENT = "BugSPY v%s" % VERSION

    COOKIE_FILE = os.path.expanduser("~/.bugspy.cookie")

    def __init__(self, bugzilla_url=None):
        self.bugzilla_url = bugzilla_url

    def get_new_bug_url(self, product):
        """Returns a quoted url for the product"""
        return "%s/%s?product=%s" % (self.bugzilla_url, self.ENTER_BUG_URL, urllib.quote(product))

    def get_bug_url(self, bug_id=None, xml=True):
        """Returns full bug url page in xml format

        Args:
            bug_id: Bug id to return with
            xml: Should it return xml web address?
        """

        if bug_id:
            if xml:
                return "%s/%s?id=%s&ctype=xml" % (self.bugzilla_url, self.SHOW_BUG_URL, bug_id)
            else:
                return "%s/%s?id=%s" % (self.bugzilla_url, self.SHOW_BUG_URL, bug_id)
        else:
            return False

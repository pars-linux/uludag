#!/usr/bin/python
# -*- coding: utf-8 -*-


# we search for specific string to understand whether we are logged in or not

class Constants:
    """Class that defines constants, both static and dynamic.

    It also automatically generates url for pages according to bugzilla_url variable so that code would be cleaner.

    Attributes:
        LOGIN_FAILED_STRING: The string to check whether we logged in or not
        SHOW_BUG_URL: Cgi script address for showing bugs

    """

    LOGIN_FAILED_STRING = "Invalid Username Or Password"
    SHOW_BUG_URL = "show_bug.cgi"

    def __init__(self, bugzilla_url=None):
        self.bugzilla_url = bugzilla_url

    def get_bug_show_page(self, bug_id=None):
        """Returns full bug show page.

        Args:
            bug_id: Bug id to return with
        """

        if bug_id:
            return "%s/%s?id=%s" % (self.bugzilla_url, self.SHOW_BUG_URL, bug_id)
        else:
            return "%s/%s" % (self.bugzilla_url, self.SHOW_BUG_URL)

#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Bugzilla tool for Pardus. I'm really bored with other distro's tools.
#
# Eren Türkay <eren:pardus.org.tr> // 21 March, 2010
#

from mechanize import Browser
import logging
import piksemel

from bugspy.error import LoginError, BugzillaError, ModifyError
from bugspy.constants import Constants
from bugspy.config import Config
from bugspy.bugparser import BugParser, BugStruct

log = logging.getLogger("bugzilla")

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


        # define constants class so that we do not mess up the code with lots of "self.bugzilla_url + "/show_bug.cgi?id=123456".
        self.constants = Constants(bugzilla_url)

        self.bugzilla_url = bugzilla_url
        self.username = username
        self.password = password

        self.browser = Browser()
        self.browser.addheaders = [("User-Agent", self.constants.USER_AGENT)]
        # disable robots txt. Pardus.org.tr has it and we cannot open any page if it is enabled. Also, kim takar yalova kaymakamını? :)
        self.browser.set_handle_robots(False)


        log.info("Bugzilla class initialised")

        # if username and password is supplied, it means we are expected to login.
        self.is_auth_needed = bool(username and password)

        self.is_logged_in = False

    def login(self):
        """Logins to bugzilla

        Returns:
            True if login is successfull. Raises exception when it fails

        Raises:
            LoginError: User or Password is wrong.
        """
        if self.is_auth_needed:
            if self.is_logged_in:
                log.debug("Already logged in, or login is not needed. Continuing..")
                return 0

            # we first need to open the page for login and other things to work
            log.info("Opening initial bugzilla webpage to login..")
            self.browser.open(self.bugzilla_url)
            log.debug("Web page is opened")

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
                logging.error("Failed to login, user or password is invalid")
                raise LoginError("User or Password is invalid")
            else:
                log.info("Successfully logged in")
                self.is_logged_in = True
                return True

    def _bug_open(self, bug_id, xml=True):
        return self.browser.open(self.constants.get_bug_url(bug_id, xml)).read()

    def get(self, bug_id):
        """Gets information about bug

        You can get everything returned from the site. See BugParser.parse() for what you get and how to use the information. If there is an error, "error" attribute contains the error msg. You should check this before continuting the program.

        bug = bugzilla.get_bug(123456)
        if bug.error:
            print "Error! Reason: %s" % bug.error
            return 0

        print bug.creation_ts
        print bug.reporter.name

        Args:
            bug_id: Bug id to get

        Returns:
            BugStruct containins bug information.
        """

        log.info("Getting bug %s" % bug_id)
        bug_data = self._bug_open(bug_id)

        bugparser = BugParser()
        return bugparser.parse(bug_data)


    def modify(self, **kwargs):
        # TODO: Implement Product/Component/Assignee/CC list
        """Modifies the bug.

        All arguments can be supplied. This function modifies the form on the page and submits just like an ordinary browser does.

        Args:
            comment: Comment to write
            status: Status (NEW, ASSIGNED, RESOLVED)
            resolution: (FIXED, INVALID, WONTFIX, LATER, REMIND, DUPLICATE)

        Raises:
            BugzillaError: You should first login to modify the bug
            ModifyError: Changes are not applied
        """

        args = BugStruct(**kwargs)

        if not args.has("bug_id"):
            raise BugzillaError("Bug id is needed to modify")

        if not self.is_logged_in:
            log.error("Login is needed")
            raise LoginError("You should first login to comment")

        log.info("Opening bug #%s to modify" % args.bug_id)

        bug_data = self._bug_open(args.bug_id, xml=False)
        # do we have permission to see this bug?
        if bug_data.find(self.constants.NO_PERMISSON_STRING) > -1:
            log.error("Don't have permission to modify the bug")
            raise BugzillaError("You don't have permission to see this bug")

        log.info("Opened bug #%s page" % args.bug_id)

        log.debug("Selecting changeform")
        self.browser.select_form(name="changeform")

        if args.has("status"):
            log.debug("Setting bug_status..")
            self.browser["bug_status"] = [args.status]

        if args.has("resolution"):
            log.debug("Setting resolution..")
            self.browser["resolution"] = [args.resolution]

        if args.has("comment"):
            log.debug("Setting comment..")
            self.browser["comment"] = args.comment

        log.info("Submitting the changes")
        response = self.browser.submit()
        response = response.read()

        # is everything alright?
        if response.find(self.constants.BUG_PROCESS_OK_STRING) > -1:
            log.info("Changes have been submitted")
            return True
        else:
            # something is wrong.
            log.error("Errr, something is wrong in returned value.")
            #print response
            raise ModifyError("Unexpected return value", response)

    # FIXME: remove it on production
    def write_file(self, file, data):
        open("/tmp/%s" % file, "w+").write(data)

def main():
    c = Config()

    bugzilla = Bugzilla(c.bugzillaurl, c.username, c.password)
    bugzilla.login()
    #bugzilla.modify_bug("12437", comment="FooBar", status="RESOLVED", solution="FIXED")

    #bugzilla.modify_bug("12437", comment="Re-opening the bug", status="REOPENED")

    bugzilla.modify_bug("12437", comment="Testing again")

if __name__ == '__main__':
    main()

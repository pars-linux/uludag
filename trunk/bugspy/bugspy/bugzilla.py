#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Bugzilla tool for Pardus. I'm really bored with other distro's tools.
#
# Eren Türkay <eren:pardus.org.tr> // 21 March, 2010
#

from mechanize import Browser
from mechanize import LWPCookieJar

import os
import re
import logging
import piksemel

from bugspy.error import LoginError, BugzillaError, ModifyError
from bugspy.constants import Constants
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
        cookiejar: Cookiejar class that mechanize uses
    """

    def __init__(self, bugzilla_url, username=None, password=None):
        """Initalises bugzilla_url, username and password variables and opens bugzilla page.

        Args:
            bugzilla_url: Bugzilla url to open
            username: Username to use. Ie. eren@pardus.org.tr
            password: Bugzilla password.
        """
        log.debug("Initialising Bugzilla class")

        # define constants class so that we do not mess up the code with lots of "self.bugzilla_url + "/show_bug.cgi?id=123456".
        self.constants = Constants(bugzilla_url)

        self.bugzilla_url = bugzilla_url
        self.username = username
        self.password = password

        self.browser = Browser()
        self.browser.addheaders = [("User-Agent", self.constants.USER_AGENT)]
        # disable robots txt. Pardus.org.tr has it and we cannot open any page if it is enabled. Also, kim takar yalova kaymakamını? :)
        self.browser.set_handle_robots(False)

        # handle cookies in a file. this will allow us to login once.
        self.cookiejar = LWPCookieJar(self.constants.COOKIE_FILE)
        self.browser.set_cookiejar(self.cookiejar)
        if self._has_cookie_file():
            log.debug("Loading cookies..")
            self._load_cookies()


        # if username and password is supplied, it means we are expected to login.
        self.is_auth_needed = bool(username and password)

        self.is_logged_in = False

        self._check_cookies()
        log.debug("Bugzilla class initialised")

    def _save_cookies(self):
        log.debug("Saving cookies...")
        self.cookiejar.save()

    def _delete_cookie_file(self):
        log.debug("Deleting cookiefile..")
        os.remove(self.constants.COOKIE_FILE)

    def _has_cookie_file(self):
        # FIXME: If cookiefile is 4 hours old. Delete it and return False
        return os.path.exists(self.constants.COOKIE_FILE)

    def _load_cookies(self):
        self.cookiejar.load()

    def _check_cookies(self):
        if self._has_cookie_file():
            log.debug("Cookie file is present, assuming we are logged in")
            self.is_logged_in = True
        else:
            self.is_logged_in = False

    def login(self):
        """Logins to bugzilla

        Returns:
            True if login is successfull. Raises exception when it fails

        Raises:
            LoginError: User or Password is wrong.
        """
        log = logging.getLogger("bugzilla.LOGIN")

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
                log.error("Failed to login, user or password is invalid")
                raise LoginError("User or Password is invalid")
            else:
                log.info("Successfully logged in")
                # save cookies for future use
                self._save_cookies()
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
        log = logging.getLogger("bugzilla.GET")

        log.info("Getting bug %s" % bug_id)
        bug_data = self._bug_open(bug_id)

        bugparser = BugParser()
        return bugparser.parse(bug_data)


    def modify(self, **kwargs):
        # TODO: Implement Product/Component/CC list
        """Modifies the bug.

        All arguments can be supplied. This function modifies the form on the page and submits just like an ordinary browser does.

        Args:
            bug_id: Bug id to edit
            title: New bug title
            comment: Comment to write
            status: Status (NEW, ASSIGNED, RESOLVED)
            resolution: (FIXED, INVALID, WONTFIX, LATER, REMIND, DUPLICATE)
            security: Whether it is security or not
            assigned_to: E-mail address to assign a bug
            blocks: Bugs that this bug blocks
            dependson: Bug that depends on.
            cc: Add e-mail address to cc list

        Raises:
            BugzillaError: You should first login to modify the bug
            ModifyError: Changes are not applied
        """
        log = logging.getLogger("bugzilla.MODIFY")

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

        # for x in self.browser.forms():
        #     print x

        if args.has("title"):
            log.debug("New title: %s" % args.title)
            self.browser["short_desc"] = args.title

        if args.has("status"):
            log.debug("Bug_status: %s" % args.status)
            self.browser["bug_status"] = [args.status]

        if args.has("resolution"):
            log.debug("Resolution: %s" % args.resolution)
            self.browser["resolution"] = [args.resolution]

        if args.has("comment"):
            log.debug("Setting comment")
            self.browser["comment"] = args.comment

        if args.has("security"):
            # Pardus has specific setting for security vulnerabilities that will not be public. The checkbox name is "bit-10"
            log.debug("Marking as security")
            if args.security == "1":
                # if the bug has bit-10 field set
                if len(self.browser["bit-10"]) != 0:
                    log.warning("Bug is already in security group, not setting security tag")
                else:
                    self.browser["bit-10"] = ["1"]
            # marking as non-security
            else:
                if len(self.browser["bit-10"]) == 0:
                    log.warning("Bug is already public, not setting security tag..")
                else:
                    self.browser["bit-10"] = []

        if args.has("assigned_to"):
            log.debug("Assigned: %s" % args.assigned_to)
            self.browser["assigned_to"] = args.assigned_to

        if args.has("dependson"):
            log.debug("Dependson: %s" % args.dependson)
            self.browser["dependson"] = args.dependson

        if args.has("blocks"):
            log.debug("Blocks: %s" % args.blocks)
            self.browser["blocked"] = args.blocks

        if args.has("cc"):
            log.debug("CC: %s" % args.cc)
            self.browser["newcc"] = args.cc

        if args.has("version"):
            log.debug("Version: %s" % args.version)
            self.browser["version"] = [args.version]

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

    def new(self, **kwargs):
        """Opens new bug

        It automatically generates bug_url from product as bugzilla wants product name in GET response

        Args:
            product: Product name in the site
            component: Component name in bugzilla page
            security: Whether it is security vulnerability
            url: External url
            status: Initial but status. (NEW, RESOLVED)
            assigned_to: Email address to assign
            alias: Bug alias (NOT IMPLEMENTED)
            blocks: Bugs that this bug blocks
            dependson: Bug that depends on.
            cc: E-mail addresses to CC

        Returns:
            Integer indicating the bugzilla id for new bug

        Raises:
            BugzillaError: Required arguments are not provided

        """
        log = logging.getLogger("bugzilla.NEW")

        args = BugStruct(**kwargs)

        # control required vars
        if not (args.has("component") and args.has("product") and args.has("title") and args.has("description")):
            raise BugzillaError("Missing argument. Component, Product, Title and Description are needed")

        bug_url = self.constants.get_new_bug_url(args.product)

        log.debug("Opening new bug page")
        self.browser.open(bug_url)
        log.debug("Selecting form name: Create")
        self.browser.select_form(name="Create")

        log.debug("Adding component, title and comment")
        self.browser["component"] = [args.component]
        self.browser["short_desc"] = args.title
        self.browser["comment"] = args.description

        if args.has("url"):
            log.debug("URL: %s" % args.url)
            self.browser["bug_file_loc"] = args.url

        if args.has("security"):
            log.debug("Security: 1")
            self.browser["bit-10"] = ["1"]

        if args.has("status"):
            log.debug("Bug_status: %s" % args.status)
            self.browser["bug_status"] = [args.status]

        if args.has("assigned_to"):
            log.debug("Assign: %s" % args.assigned_to)
            self.browser["assigned_to"] = args.assigned_to

        if args.has("dependson"):
            log.debug("Depends on: %s" % args.dependson)
            self.browser["dependson"] = args.dependson

        if args.has("blocks"):
            log.debug("Blocks: %s" % args.blocks)
            self.browser["blocked"] = args.blocks

        if args.has("version"):
            log.debug("Version: %s" % args.version)
            self.browser["version"] = [args.version]

        if args.has("cc"):
            log.debug("CC: %s" % args.cc)
            self.browser["cc"] = args.cc

        # FIXME: Our bugzilla page doesn't show alias field. 
        # FIXME: Uncomment it when it is done
        # if args.has("alias"):
        #     self.browser["alias"] = args.alias

        response = self.browser.submit()
        response = response.read()

        log.info("Bug submitted")

        # get bug id.
        re_compile = re.compile("Bug (.*?) Submitted")
        bug_id = re.findall(re_compile, response)

        if len(bug_id) != 0:
            return bug_id[0]
        else:
            log.error("Wohoops. Unexpected data returned after submitting.")
            return False


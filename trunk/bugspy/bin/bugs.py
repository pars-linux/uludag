#!/usr/bin/python
# -*- coding: utf-8 -*-

# This file will be useable executable

import logging
import sys
import os
import optparse

from bugspy.bugzilla import Bugzilla
from bugspy.config import Config
from bugspy.bugparser import BugStruct
from bugspy.error import BugzillaError

log = logging.getLogger("bugzilla")
if "--debug" in sys.argv:
    log.setLevel(logging.DEBUG)
elif "--verbose" in sys.argv:
    log.setLevel(logging.INFO)
else:
    log.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
#ch.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s"))
ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

log.addHandler(ch)

cmdlist = ["info", "modify", "generate-config"]

# CONSTANTS

CONFIG_TEMPLATE = """[General]
bugzillaUrl = %(bugzilla)s

[Auth]
username = %(user)s
password = %(password)s
"""

CONFIG_FILE = "%s/.bugspy.conf" % os.environ["HOME"]

VALID_RESOLUTIONS = ["FIXED", "INVALID", "WONTFIX", "LATER", "REMIND", "DUPLICATE"]
VALID_STATUSES = ["REOPENED", "NEW", "ASSIGNED", "RESOLVED"]

def setup_parser():
    u =   "usage: %prog [global options] COMMAND [options]"
    u +=  "\nCommands: %s" % ', '.join(cmdlist)

    p = optparse.OptionParser(usage=u)
    p.disable_interspersed_args()
    # General bugzilla connection options
    p.add_option("--verbose",action="store_true",
            help="give more info about what's going on")
    p.add_option("--debug",action="store_true",
            help="output bunches of debugging info")

    return p

def setup_action_parser(action):
    p = optparse.OptionParser(usage="usage: %%prog %s [options]" % action)

    if action == "modify":
        p.add_option("-b", "--bug",
                metavar="BUG ID", dest="bug_id",
                help="REQUIRED: bug id")

        p.add_option("-c", "--comment",
                help="OPTIONAL: add comment")

        p.add_option("-s", "--status",
                help="OPTIONAL: set status (%s)" % ','.join(VALID_STATUSES))

        p.add_option("-r", "--resolution",
                help="OPTIONAL: set resolution (%s)" % ','.join(VALID_RESOLUTIONS))

    if action == "generate-config":
        p.add_option("-b", "--bugzilla",
                action="store", type="string", metavar="BUGZILLA URL", dest="bugzilla_url",
                help="REQUIRED: Bugzilla URL to use. Do not append the last slash. E.g: http://bugs.pardus.org.tr")

        p.add_option("-u", "--user", action="store", type="string",
                help="REQUIRED: Username. E.g: eren@pardus.org.tr")

        p.add_option("-p", "--password", action="store", type="string",
                help="REQUIRED: Password")

    return p

def main():
    parser = setup_parser()
    (global_opts, args) = parser.parse_args()

    global_opts = BugStruct(**global_opts.__dict__)

    # Get our action from these args
    if len(args) and args[0] in cmdlist:
        action = args.pop(0)
    else:
        parser.error("command must be one of: %s" % ','.join(cmdlist))

    action_parser = setup_action_parser(action)
    (opt, args) = action_parser.parse_args(args)
    opt = BugStruct(**opt.__dict__)

    if not os.path.exists(CONFIG_FILE) and action != "generate-config":
        log.error("Configuation file is not found, please generate it first")
        sys.exit(1)

    c = Config()
    bugzilla = Bugzilla(c.bugzillaurl, c.username, c.password)

    if action == "generate-config":
        if os.path.exists(CONFIG_FILE):
            log.warning("Configuration file exists. Please edit ~/.bugspy.conf with your text editor. Exiting...")
            sys.exit(1)

        # check arguments
        if not (opt.user and opt.password and opt.bugzilla_url):
            log.error("Missing argument! See --help")
            sys.exit(1)

        config_data = CONFIG_TEMPLATE % {"bugzilla": opt.bugzilla_url,
                                         "user": opt.user,
                                         "password": opt.password}

        log.info("Writing configuration file")
        open(CONFIG_FILE, "w+").write(config_data)
        log.info("Configuration file is written. You can edit ~/.bugspy.conf for later use")

    if action == "modify":
        modify = {}
        if not opt.bug_id:
            log.error("Bud id must be provided!")
            sys.exit(1)

        modify["bug_id"] = opt.bug_id

        if opt.comment:
            modify["comment"] = opt.comment

        if opt.resolution:
            # make it upper-case for easy-of-use
            opt.resolution = opt.resolution.upper()
            if not opt.resolution in VALID_RESOLUTIONS:
                parser.error("resolution must be one of: %s" % ','.join(VALID_RESOLUTIONS))
                sys.exit(1)

            # we cannot set resolution on NEW bugs
            bugzilla.login()
            bug_info = bugzilla.get(opt.bug_id)
            if bug_info.has("status") and bug_info.status == "NEW":
                log.error("You cannot change resolution on NEW bugs. Maybe you want to this?: --status RESOLVED --resolution %s" % opt.resolution)
                sys.exit(1)

            modify["resolution"] = opt.resolution

        if opt.status:
            # make it upper-case for easy-of-use
            opt.status = opt.status.upper()

            if not opt.status in VALID_STATUSES:
                parser.error("status must be one of: %s" % ','.join(VALID_STATUSES))

            if opt.status == "RESOLVED" and not opt.resolution:
                parser.error("RESOLVED should be used along with RESOLUTION.")
                sys.exit(1)

            modify["status"] = opt.status


        try:
            bugzilla.login()
            bugzilla.modify(**modify)
        except BugzillaError, e:
            log.error(e.msg)

if __name__ == '__main__':
    main()

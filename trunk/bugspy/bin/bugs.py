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

log = logging.getLogger("bugzilla")
if "--debug" in sys.argv:
    log.setLevel(logging.DEBUG)
elif "--verbose" in sys.argv:
    log.setLevel(logging.INFO)
else:
    log.setLevel(logging.WARNING)

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

    if action == "generate-config":
        #if os.path.exists(CONFIG_FILE):
        #    log.warning("Configuration file exists, exiting..")
        #    sys.exit(1)

        # check arguments
        if not (opt.user and opt.password and opt.bugzilla_url):
            log.error("Missing argument! See --help")
            sys.exit(1)

    #c = Config()

   # bugzilla = Bugzilla(c.bugzillaurl, c.username, c.password)
    #bugzilla.login()
    #print bugzilla.get_bug("9901")

if __name__ == '__main__':
    main()

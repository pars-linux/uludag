#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import os
import sys
import ConfigParser

from ahenk.ajan import mainloop


if __name__ == "__main__":

    # Command line options
    parser = optparse.OptionParser()
    parser.add_option("-c", "--config", dest="conffile", default="/etc/ahenk-ajan.conf",
                      help="Use alternate configuration file", metavar="FILE")
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon",
                      help="Run as a daemon.")
    parser.add_option("-k", "--kill", action="store_true", dest="kill",
                      help="Kill running daemon.")
    parser.add_option("-n", "--dry-run", action="store_true", dest="dryrun",
                      help="Do nothing, just tell.")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="Verbose mode")
    (options, args) = parser.parse_args()

    # Only root can run that application
    if os.getuid() != 0:
        print "%s must be run as root." % sys.argv[0]
        sys.exit(1)

    # Normalize configuration file path
    options.conffile = os.path.realpath(options.conffile)

    if not os.path.exists(options.conffile):
        print "%s is missing." % options.conffile
        sys.exit(1)

    # Read configuration file
    cp = ConfigParser.ConfigParser()
    try:
        cp.read(options.conffile)
    except IOError:
        print "%s is corrupted." % options.conffile
        sys.exit(1)

    # Host and domain names are mandatory.
    if not cp.has_option("server", "hostname"):
        print "No Ahenk-Server address defined in %s" % options.conffile
        sys.exit(1)
    if not cp.has_option("server", "domain"):
        print "No domainname defined in %s" % options.conffile
        sys.exit(1)

    options.hostname = cp.get("server", "hostname")
    options.domain = cp.get("server", "domain")

    # Username and password must be used together
    if cp.has_option("server", "username") and cp.has_option("server", "password"):
        options.username = cp.get("server", "username")
        options.password = cp.get("server", "password")
    else:
        options.username = None
        options.password = None

    # Policy check interval, default is 60 seconds
    if cp.has_option("server", "interval"):
        options.interval = int(cp.get("server", "interval"))
    else:
        options.interval = 60

    # PID file
    if cp.has_option("general", "pidfile"):
        options.pidfile = cp.get("general", "pidfile")
    else:
        options.pidfile = "/var/run/ahenk-ajan.pid"

    # Log file
    if cp.has_option("general", "logfile"):
        options.logfile = cp.get("general", "logfile")
    else:
        options.logfile = "/var/run/ahenk-ajan.pid"

    # Modules directory
    if cp.has_option("general", "moddir"):
        options.moddir = cp.get("general", "moddir")
    else:
        options.moddir = "/var/lib/ahenk-ajan/"
    if not os.path.exists(options.moddir):
        os.makedirs(options.moddir)

    # Policy cache directory
    if cp.has_option("general", "policydir"):
        options.policydir = cp.get("general", "policydir")
    else:
        options.policydir = "/var/db/ahenk-ajan/"
    if not os.path.exists(options.policydir):
        os.makedirs(options.policydir)

    # It's time to enter the main loop:
    if options.daemon:
        daemon = mainloop.Ajan(options)
        if options.kill:
            daemon.stop()
        else:
            daemon.start()
    elif not options.kill:
        # Interactive mode for debugging
        daemon = mainloop.Ajan(options)
        daemon.run()

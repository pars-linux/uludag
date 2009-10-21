#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
import os
import sys

from ahenk.ajan import mainloop

if __name__ == "__main__":

    parser = optparse.OptionParser()

    parser.add_option("-c", "--config", dest="conffile", default="/etc/ahenk-ajan.conf",
                      help="Use alternate configuration file", metavar="FILE")
    parser.add_option("-d", "--daemon", action="store_true", dest="daemon",
                      help="Run as a daemon.")
    parser.add_option("-k", "--kill", action="store_true", dest="kill",
                      help="Kill running daemon.")
    parser.add_option("-l", "--logfile", dest="logfile", default="/var/log/ahenk-ajan.log",
                      help="Use alternate log file", metavar="FILE")
    parser.add_option("-m", "--moddir", dest="moddir", default="/var/lib/ahenk-ajan",
                      help="Use alternate module directory", metavar="DIR")
    parser.add_option("-p", "--pidfile", dest="pidfile", default="/var/run/ahenk-ajan.pid",
                      help="Use alternate PID file", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
                      help="Verbose mode")

    (options, args) = parser.parse_args()

    if os.getuid() != 0:
        print "%s must be run as root." % sys.argv[0]
        sys.exit(1)

    options.conffile = os.path.realpath(options.conffile)
    options.logfile = os.path.realpath(options.logfile)
    options.moddir = os.path.realpath(options.moddir)
    options.pidfile = os.path.realpath(options.pidfile)

    if options.daemon:
        daemon = mainloop.Ajan(options)
        if options.kill:
            daemon.stop()
        else:
            daemon.start()
    else:
        # Interactive mode for debugging
        daemon = mainloop.Ajan(options)
        daemon.run()

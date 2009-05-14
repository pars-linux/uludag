# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys

import pisi
import pisi.context as ctx
import pisi.ui
import pisi.util

class Error(pisi.Error):
    pass

class Exception(pisi.Exception):
    pass

def printu(obj, err = False):
    if not isinstance(obj, unicode):
        obj = unicode(obj)
    if err:
        out = sys.stderr
    else:
        out = sys.stdout
    out.write(obj.encode('utf-8'))
    out.flush()



class CLI(pisi.ui.UI):
    "Command Line Interface special to buildfarm"

    def __init__(self, output, show_debug=False, show_verbose=False):
        super(CLI, self).__init__(show_debug, show_verbose)
        self.warnings = 0
        self.errors = 0
        self.output_file = output

        self.outtypes = {'Warning'  : ('brightyellow', 'brightyellow'),
                         'Error'    : ('red', 'red'),
                         'Action'   : ('green', 'green'),
                         'Notify'   : ('cyan', 'cyan'),
                         'Status'   : ('brightgreen', 'brightgreen'),
                         'Display'  : ('gray', 'gray')}

    def close(self):
        pisi.util.xterm_title_reset()

    def format(self, msg, msgtype, colored=True):
        result = ""
        if not ctx.get_option('no_color'):
            if msgtype == 'Display':
                result = msg
            elif colored and self.outtypes.has_key(msgtype):
                result = pisi.util.colorize(msg + '\n', self.outtypes[msgtype][0])
            else:
                result = msg + '\n'
        else:
            result = msgtype + ': ' + msg + '\n'

        return result

    def output(self, msg, msgtype=None, err=False, verbose=False):
        if (verbose and self.show_verbose) or (not verbose):
            if type(msg)==type(unicode()):
                msg = msg.encode('utf-8')
            if err:
                out = sys.stderr
            else:
                out = sys.stdout

            # Output to screen
            out.write(self.format(msg, msgtype))
            out.flush()

            # Output the same stuff to the log file
            self.output_file.write(self.format(msg, msgtype, False))
            self.output_file.flush()

    def info(self, msg, verbose=False, noln=False):
        self.output(unicode(msg), 'Info', verbose=verbose)

    def warning(self, msg):
        msg = unicode(msg)
        self.warnings += 1
        if ctx.log:
            ctx.log.warning(msg)

        self.output(msg, 'Warning', err=True, verbose=False)

    def error(self, msg):
        msg = unicode(msg)
        self.errors += 1
        if ctx.log:
            ctx.log.error(msg)

        self.output(msg, 'Error', err=True)

    def action(self, msg):
        msg = unicode(msg)
        if ctx.log:
            ctx.log.info(msg)

        self.output(msg, 'Action')

    def choose(self, msg, opts):
        msg = unicode(msg)
        prompt = msg + pisi.util.colorize(' (%s)' % "/".join(opts), 'red')
        while True:
            s = raw_input(prompt.encode('utf-8'))
            for opt in opts:
                if opt.startswith(s):
                    return opt

    def confirm(self, msg):
        # Modify so that it always returns True in buildfarm
        return True

    def display_progress(self, **ka):
        """ display progress of any operation """
        if ka['operation'] in ["removing", "rebuilding-db"]:
            return
        elif ka['operation'] == "fetching":
            totalsize = '%.1f %s' % pisi.util.human_readable_size(ka['total_size'])
            out = '\r%-30.50s (%s)%3d%% %9.2f %s [%s]' % \
                (ka['filename'], totalsize, ka['percent'],
                 ka['rate'], ka['symbol'], ka['eta'])
            self.output(out, 'Display')
        else:
            self.output("\r%s (%d%%)" % (ka['info'], ka['percent']), 'Display')

        if ka['percent'] == 100:
            self.output(' [complete]\n', 'Display')

    def status(self, msg = None):
        if msg:
            msg = unicode(msg)
            self.output(msg, 'Status')
            pisi.util.xterm_title(msg)

    def notify(self, event, **keywords):
        if event == pisi.ui.installed:
            msg = 'Installed %s' % keywords['package'].name
        elif event == pisi.ui.removed:
            msg = 'Removed %s' % keywords['package'].name
        elif event == pisi.ui.upgraded:
            msg = 'Upgraded %s' % keywords['package'].name
        elif event == pisi.ui.configured:
            msg = 'Configured %s' % keywords['package'].name
        elif event == pisi.ui.extracting:
            msg = 'Extracting the files of %s' % keywords['package'].name
        else:
            msg = None
        if msg:
            self.output(msg, 'Notify')
            if ctx.log:
                ctx.log.info(msg)

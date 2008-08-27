# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

__version__ = "2.0.1"

import sys
import exceptions
import traceback
import cStringIO

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import pisi
from yali4.exception import *

def default_runner():
    """ Main runner of YALI """
    import yali4.gui.runner

    sys.excepthook = exception_handler

    return yali4.gui.runner.Runner()

exception_normal, exception_fatal, \
    exception_pisi, exception_informational, \
    exception_unknown = range(5)

def exception_handler(exception, value, tb):
    """ YALI exception handler for showing exceptions in GUI """

    exception_type = exception_unknown

    if isinstance(value, YaliError):
        exception_type = exception_fatal

    elif isinstance(value, pisi.Error):
        exception_type = exception_pisi

    elif isinstance(value, YaliException):
        exception_type = exception_normal

    elif isinstance(value, YaliExceptionInfo):
        exception_type = exception_informational


    sio = cStringIO.StringIO()

    v = ''
    for e in value.args:
        v += str(e) + '\n'
    sio.write(v)

    if exception_type != exception_informational:
        sio.write(str(exception))
        sio.write('\n\n')
        sio.write(_("Backtrace:"))
        sio.write('\n')
        traceback.print_tb(tb, None, sio)

    sio.seek(0)

    import yali4.gui.runner
    yali4.gui.runner.showException(exception_type, unicode(sio.read()))

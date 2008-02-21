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

from os.path import join, exists
import codecs

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.gui.context as ctx
from yali4.gui.GUIException import *

##
# GPL widget
class Widget(QTextBrowser):

    def __init__(self, *args):
        apply(QTextBrowser.__init__, (self,) + args)

        self.setSizePolicy( QSizePolicy(QSizePolicy.Preferred,
                                        QSizePolicy.Expanding))

        try:
            self.setText(codecs.open(self.find_license_file(), "r", "UTF-8").read())
        except Exception, e:
            raise GUIException, e

    def find_license_file(self):
        f = join(ctx.consts.source_dir,
                 "license/license-" + ctx.consts.lang + ".txt")
        if not exists(f):
            # TODO: log that license translation is not present.
            f = join(ctx.consts.source_dir,
                     "license/license-en.txt")

        if exists(f):
            return f
        else:
            raise GUIException, _("Can't open License file!")

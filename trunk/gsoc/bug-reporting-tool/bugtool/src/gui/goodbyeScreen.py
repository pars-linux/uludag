# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


import tempfile
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n
from bugz.config import config
from urlparse import urljoin

from gui.ScreenWidget import ScreenWidget
from gui.goodbyeWidget import Ui_bugWidget
from gui.credentialsScreen import BUGZILLA_URL


BUG_PRODUCT = 'FoodReplicator'
BUG_COMPONENT = 'SpiceDispenser'
BUG_VERSION = '1.0'
FEATURE_PRODUCT = ''
FEATURE_COMPONENT = ''
FEATURE_VERSION = ''


class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Bug Reporting Tool")
    desc = ki18n("Goodbye Screen")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_bugWidget()
        self.ui.setupUi(self)
        self.bug_submitted = False

    def shown(self):
        if not self.bug_submitted:
            bugz = self.shared['bugzilla']
            title = self.shared['summary']
            description = self.shared['description']
            product = FEATURE_PRODUCT
            component = FEATURE_COMPONENT
            data = {'version': FEATURE_VERSION}
            if self.shared['type'] == 'bug':
                product = BUG_PRODUCT
                component = BUG_COMPONENT
                data['version'] = BUG_VERSION

            bid = bugz.post(product, component, title, description, **data)
            if bid == 0:
                raise RuntimeError, 'Error submitting bug to %s' % BUGZILLA_URL

            url = '%s?id=%d' % (urljoin(BUGZILLA_URL, config.urls['show']),
                                bid)
            print url
            self.ui.linkText.setText('You can view your report online by '
                                     'clicking <a href=%s>here</a>' % url)

            # sumbitting attachments
            files = self.shared['attachments']
            for k in files:
                tmp = tempfile.NamedTemporaryFile()
                filename, mime, content = files[k]
                tmp.write(content)
                tmp.flush()
                tmp.seek(0)
                res = bugz.attach(bid, filename, k, tmp.name, mime, filename)
                if not res:
                    raise RuntimeError, 'Error uploading file %s' % filename
            self.bug_submitted = True

    def execute(self):
        return True

    @property
    def shared(self):
        return self.parent().parent().parent().shared_data


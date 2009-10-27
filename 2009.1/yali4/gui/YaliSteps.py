# -*- coding: utf-8 -*-
#
# Copyright (C) 2007-2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import time
import yali4.gui.context as ctx

class YaliSteps:
    def __init__(self):
        self.items = []

    def setOperations(self, stepItems):
        for item in stepItems:
            _item = stepItem(item["text"],item["operation"])
            self.items.append(_item)

    def slotRunOperations(self):
        for item in self.items:
            if not item.status:
                item.runOperation()
                time.sleep(0.5)

class stepItem:
    def __init__(self,text,operation):
        self.text = text
        self.operation = operation
        self.status = False

    def runOperation(self):
        self.status = self.operation()
        ctx.debugger.log("Running step : %s" % self.text)
        ctx.yali.info.updateAndShow(self.text)
        if self.status:
            ctx.debugger.log("Step '%s' finished sucessfully." % self.text)
        else:
            ctx.debugger.log("Step '%s' finished with failure." % self.text)


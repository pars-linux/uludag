# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from khtml import DOM
from kdecore import i18n

class CustomEventListener(DOM.EventListener):
    def __init__(self, parent):
        DOM.EventListener.__init__(self)
        self.parent = parent

    def handleEvent(self,event):
        target = event.target().nodeName().string()
        try:
            #if checkbox is clicked, call SpecialList's slot
            if target == "INPUT":
                inputElement = DOM.HTMLInputElement(event.target())
                name = inputElement.name().string()
                checked = inputElement.checked()

                # call parent to handle click event (in fact, parent emits this as a signal and its parent handles the signal)
                self.parent.slotCheckboxClicked(name, checked)

            elif target == "A":
                link = event.target().attributes().getNamedItem(DOM.DOMString("href")).nodeValue().string()
                if link == "#selectall":
                    state = event.target().firstChild().nodeValue().string()
                    reverseSelection = False
                    if state == i18n("Select all packages in this category"):
                        event.target().firstChild().setNodeValue(DOM.DOMString(i18n("Reverse package selections")))
                    else:
                        reverseSelection = True
                        event.target().firstChild().setNodeValue(DOM.DOMString(i18n("Select all packages in this category")))

                    # let the list do the rest
                    self.parent.slotSelectAll(reverseSelection)
                else:
                    self.parent.slotHomepageClicked(link)
        except Exception, e:
            print "Exception: " + str(e)

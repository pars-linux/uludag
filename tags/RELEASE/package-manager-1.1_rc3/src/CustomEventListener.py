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
from kdecore import i18n, KURL
from kio import KRun

class CustomEventListener(DOM.EventListener):
    def __init__(self, parent):
        DOM.EventListener.__init__(self)
        self.parent = parent
        self.selectingAll = False

    def handleEvent(self,event):
        target = event.target().nodeName().string()
        try:
            if target == "INPUT":
                inputElement = DOM.HTMLInputElement(event.target())
                name = inputElement.name().string()
                checked = inputElement.checked()
                if checked:
                    if name not in self.parent.basket.packages:
                        self.parent.basket.add(name)
                else:
                    self.parent.basket.remove(name)

                self.parent.updateButtons()
                if not self.selectingAll:
                    self.parent.updateStatusBar()

            elif target == "A":
                link = event.target().attributes().getNamedItem(DOM.DOMString("href")).nodeValue().string()
                if link == "#selectall":
                    document = self.parent.htmlPart.document()
                    nodeList = document.getElementsByTagName(DOM.DOMString("input"))

                    state = event.target().firstChild().nodeValue().string()
                    reverseSelection = False
                    if state == i18n("Select all packages in this category"):
                        event.target().firstChild().setNodeValue(DOM.DOMString(i18n("Reverse package selections")))
                    else:
                        reverseSelection = True
                        event.target().firstChild().setNodeValue(DOM.DOMString(i18n("Select all packages in this category")))

                    self.selectingAll = True
                    for i in range(0,nodeList.length()):
                        element = DOM.HTMLInputElement(nodeList.item(i))
                        if reverseSelection or not element.checked():
                            element.click()
                    self.selectingAll = False
                    self.parent.updateStatusBar()
                else:
                    KRun.runURL(KURL(link),"text/html",False,False);
        except Exception, e:
            print e

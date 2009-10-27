#!/usr/bin/python
# -*- coding: utf-8 -*-

#qt import
from qt import *

#kde imports
from kdecore import *
from kdeui import *
from khtml import *
from kio import KRun

import pisi
import re
import string

import Globals
import CustomEventListener
from Icons import *

class SpecialList(QObject):
    def __init__(self, parent):
        QObject.__init__(self)
        self.parent = parent
        self.part = KHTMLPart(self.parent)
        self.part.view().setFocus()
        self.selectingAll = False

        # Read javascript
        js = file(str(locate("data","package-manager/animation.js"))).read()
        js = re.sub("#3cBB39", KGlobalSettings.alternateBackgroundColor().name(), js)
        js = re.sub("#3c8839", KGlobalSettings.baseColor().name(), js)
        self.javascript = re.sub("#533359",KGlobalSettings.highlightColor().name(), js)

        # Read Css
        cssFile = file(str(locate("data","package-manager/layout.css"))).read()
        self.css = cssFile

        self.connect(self.part, SIGNAL("completed()"), self.registerEventListener)

    def registerEventListener(self):
        self.eventListener = CustomEventListener.CustomEventListener(self)
        node = self.part.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

    def slotCheckboxClicked(self, itemName, checked):
        if not self.selectingAll:
            self.emit(PYSIGNAL("checkboxClicked"), (itemName, checked))

    def slotHomepageClicked(self, link):
        KRun.runURL(KURL(link),"text/html",False,False);

    def slotSelectAll(self, reverse):
        document = self.part.document()
        nodeList = document.getElementsByTagName(DOM.DOMString("input"))

        self.selectingAll = True
        for i in range(0, nodeList.length()):
            element = DOM.HTMLInputElement(nodeList.item(i))
            if reverse or not element.checked():
                element.click()
        self.selectingAll = False

        #TODO: Fix this
        #self.parent.updateStatusBar()

    def clear(self):
        self.part.view().setContentsPos(0, 0)
        self.part.begin()
        self.part.write('''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        </head>
        <body/>
        ''')
        self.part.end()

    def createList(self, packages, part = None, selected = [], disabled = []):
        head =  '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        '''

        if not part:
            part = self.part

        self.selected = selected
        self.disabled = disabled

        Globals.setWaitCursor()
        part.view().setContentsPos(0, 0)
        part.begin()
        part.write(head)
        part.write("<style type=\"text/css\">%s</style>" % self.css)
        part.write("<script language=\"JavaScript\">%s</script>" % self.javascript)
        part.write("</head><body>")

        if set(packages) - set(selected):
            part.write('''<font size="-2"><a href="#selectall">'''+i18n("Select all packages in this category")+'''</a></font>''')
        else:
            part.write('''<font size="-2"><a href="#selectall">'''+i18n("Reverse package selections")+'''</a></font>''')

        part.write(self.createListForPackages(packages))
        part.end()
        Globals.setNormalCursor()

    def createListForPackages(self, packages):
        result = ""
        template ='''
        <!-- package start -->
        <div>
        <!-- checkbox --> %s <!-- checkbox -->
        <div class="package_title" style="%s" id="package_t%d" onclick="showHideContent(this)">
        <img src="%s" style="float:left;" width="%dpx" height="%dpx">
        <b>%s</b><br><span style="color:#303030">%s</span><br>
        </div>
        <div class="package_info" style="%s" id="package_i%d">
        <div style="margin-left:25px;" class="package_info_content" id="package_ic%d">
        <p><b>%s</b>
        %s<br>
        <b>%s</b>%s<br><b>%s</b>%s<br><b>%s</b>%s<br><b>%s</b><a href=\"%s\">%s</a>
        </p>
        </div>
        </div>
        </div>
        <!-- package end -->
        '''

        index = 0
        titleStyle = ""
        style = ""

        packages.sort(key=string.lower)

        alternativeColor = KGlobalSettings.alternateBackgroundColor().name()
        baseColor = KGlobalSettings.baseColor().name()

        for app in packages:
            if index % 2 == 0:
                style = "background-color:%s" % alternativeColor
            else:
                style = "background-color:%s" % baseColor
            titleStyle = style

            if app.name in self.selected:
                titleStyle = "background-color:#678DB2"
                checkState = "checked"
            else:
                checkState = ""

            curindex = index + 1
            if app.name in self.disabled:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           disabled %s name="%s id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app,curindex)
            else:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           %s onclick="changeBackgroundColor(this)" name="%s" id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app,curindex)

            iconSize = getIconSize()
            result += template % (checkbox, titleStyle, curindex, app.icon_path, iconSize, iconSize, app.name, app.summary, style, curindex, curindex,
                                  i18n("Description: "), app.description,
                                  i18n("Version: "), app.version,
                                  i18n("Repository: "), app.repo,
                                  i18n("Package Size: "), app.size,
                                  i18n("Homepage: "), app.homepage, app.homepage)
            index += 1

        return result


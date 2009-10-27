#!/usr/bin/python
# -*- coding: utf-8 -*-

#qt import
from qt import *

#kde imports
from kdecore import *
from kdeui import *
from khtml import *
from kio import KRun

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
        js = re.sub("#3cBB39", str(KGlobalSettings.alternateBackgroundColor().name()), js)
        js = re.sub("#3c8839", str(KGlobalSettings.baseColor().name()), js)
        self.javascript = re.sub("#533359",str(KGlobalSettings.highlightColor().name()), js)

        # Read Css
        cssFile = file(str(locate("data","package-manager/layout.css"))).read()
        self.css = cssFile

        self.connect(self.part, SIGNAL("completed()"), self.registerEventListener)

    def registerEventListener(self):
        self.eventListener = CustomEventListener.CustomEventListener(self)
        node = self.part.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

    def slotCheckboxClicked(self, itemName, checked):
        self.emit(PYSIGNAL("checkboxClicked"), (itemName, checked))

        if not self.selectingAll:
            self.parent.parent().updateAfterAPackageClicked()

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
        self.parent.parent().updateAfterAPackageClicked()

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
        try:
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

        finally:
            Globals.setNormalCursor()

    def createListForPackages(self, packages):
        result = ""
        template ='''
        <!-- package start -->
        <div>
        <!-- checkbox --> %s <!-- checkbox -->
        <div class="package_title" style="%s" id="package_t%d" onclick="showHideContent(this)">
        <img src="%s" style="float:left;" width="%dpx" height="%dpx">
        <b>%s</b><br><span style="color:%s">%s</span><br>
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

        packages.sort(lambda x,y: x.name.lower() > y.name.lower() or (x.name.lower() < y.name.lower() and -1))

        alternativeColor = KGlobalSettings.alternateBackgroundColor().name()
        baseColor = KGlobalSettings.baseColor().name()
        selectedBaseColor = "#678DB2"
        summaryColor = "#303030"

        for app in packages:
            if index % 2 == 0:
                style = "background-color:%s" % alternativeColor
            else:
                style = "background-color:%s" % baseColor
            titleStyle = style

            if app.name in self.selected:
                titleStyle = "background-color:%s" % selectedBaseColor
                checkState = "checked"
            else:
                checkState = ""

            curindex = index + 1
            if app.name in self.disabled:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           disabled %s name="%s id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app.name,curindex)
            else:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           %s onclick="changeBackgroundColor(this)" name="%s" id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app.name,curindex)

            iconSize = getIconSize()
            iconPath = getIconPath(app.icon)
            result += template % (checkbox, titleStyle, curindex, iconPath, iconSize, iconSize, app.name, summaryColor, app.summary, style, curindex, curindex,
                                  i18n("Description: "), app.description,
                                  i18n("Version: "), app.version,
                                   i18n("Repository: "), app.repo,
                                   i18n("Package Size: "), Globals.humanReadableSize(app.size),
                                  i18n("Homepage: "), app.source.homepage, app.source.homepage)
            index += 1

        return result


#!/usr/bin/python
# -*- coding: utf-8 -*-

#qt import
from qt import *

#kde imports
from kdecore import *
from kdeui import *
from khtml import *

import pisi
import re

import Globals
import CustomEventListener

class SpecialList:
    def __init__(self, parent):
        self.parent = parent
        self.part = KHTMLPart(self.parent)
        self.part.view().setFocus()
        
        # Read javascript
        js = file(str(locate("data","package-manager/animation.js"))).read()
        js = re.sub("#3cBB39", KGlobalSettings.alternateBackgroundColor().name(), js)
        js = re.sub("#3c8839", KGlobalSettings.baseColor().name(), js)
        self.javascript = re.sub("#533359",KGlobalSettings.highlightColor().name(), js)

        # Read Css
        cssFile = file(str(locate("data","package-manager/layout.css"))).read()
        self.css = cssFile

        QObject.connect(self.part, SIGNAL("completed()"), self.registerEventListener)
    
    def registerEventListener(self):
        self.eventListener = CustomEventListener.CustomEventListener(self)
        node = self.part.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

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

    def createList(self,packages,part=None):
        head =  '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        '''

        if not part:
            part = self.part

        Globals.setWaitCursor()
        part.view().setContentsPos(0, 0)
        part.begin()
        part.write(head)
        part.write("<style type=\"text/css\">%s</style>" % self.css)
        part.write("<script language=\"JavaScript\">%s</script>" % self.javascript)
        part.write("</head><body>")

        if set(packages) - set(self.basket.packages):
            part.write('''<font size="-2"><a href="#selectall">'''+i18n("Select all packages in this category")+'''</a></font>''')
        else:
            part.write('''<font size="-2"><a href="#selectall">'''+i18n("Reverse package selections")+'''</a></font>''')

        part.write(self.createListForPackages(packages))
        part.end()
        Globals.setNormalCursor()

    def createListForPackages(self,packages):
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
        pdb = pisi.db.packagedb.PackageDB()

        alternativeColor = KGlobalSettings.alternateBackgroundColor().name()
        baseColor = KGlobalSettings.baseColor().name()

        for app in packages:
            if index % 2 == 0:
                style = "background-color:%s" % alternativeColor
            else:
                style = "background-color:%s" % baseColor
            titleStyle = style

            size = 0L
            if self.state == remove_state:
                # first try to locate package information from repository databases
                try:
                    package, repo = pdb.get_package_repo(app)
                #TODO: Handle "Repo item not found" type of exceptions only
                except:
                    # if it fails use provided information directly
                    #package = pdb.get_package(app, pisi.itembyrepodb.installed)
                    package = pisi.db.installdb.InstallDB().get_package(app)
                    repo = i18n("N\A")
                size = package.installedSize
            else:
                package, repo = pdb.get_package_repo(app)
                size = package.packageSize

            desc = package.description
            summary = package.summary
            version = package.version
            iconPath = getIconPath(package.icon)

            if package.source:
                homepage = package.source.homepage
            else:
                homepage = i18n("N\A")

            if size:
                tpl = pisi.util.human_readable_size(size)
                size = "%.0f %s" % (tpl[0], tpl[1])
            else:
                size = i18n("N\A")

            if app in self.basket.packages:
                titleStyle = "background-color:#678DB2"
                checkState = "checked"
            else:
                checkState = ""

            curindex = index + 1
            if self.state == remove_state and app in unremovable_packages:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           disabled %s name="%s id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app,curindex)
            else:
                checkbox = """<div class="checkboks" style="%s" id="checkboks_t%d"><input type="checkbox" \
                           %s onclick="changeBackgroundColor(this)" name="%s" id="checkboks%d"></div>""" % (titleStyle,curindex,checkState,app,curindex)

            iconSize = getIconSize()
            result += template % (checkbox, titleStyle,curindex,iconPath,iconSize,iconSize,app,summary,style,curindex,curindex,
                                  i18n("Description: "), desc,
                                  i18n("Version: "), version,
                                  i18n("Repository: "), repo,
                                  i18n("Package Size: "), size,
                                  i18n("Homepage: "), homepage,homepage)
            index += 1

        return result


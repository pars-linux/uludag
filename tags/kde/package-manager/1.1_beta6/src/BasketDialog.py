import string

from sets import Set as set
from qt import *
from kdecore import *
from khtml import *

import pisi

(install_state, remove_state, upgrade_state) = range(3)

def getIconPath(name, group=KIcon.Desktop):
    if not name:
        name = "package"
    return KGlobal.iconLoader().iconPath(name,group)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

class SelectEventListener(DOM.EventListener):
    def __init__(self, parent):
        DOM.EventListener.__init__(self)
        self.parent = parent

    def handleEvent(self,event):
        target = event.target().nodeName().string()
        try:
            if target == "INPUT":
                inputElement = DOM.HTMLInputElement(event.target())
                name = inputElement.name().string()
                checked = inputElement.checked()
                if checked:
                    if name not in self.parent.packages:
                        self.parent.packages.append(str(name))
                else:
                    self.parent.packages.remove(str(name))

                self.parent.updateTotals()
        except Exception, e:
            print e

class BasketDialog(QDialog):
    def __init__(self, parent, packages, state):
        QDialog.__init__(self,parent,str(i18n("Basket")),True)

        self.packages = packages
        self.state = state
        self.totalSize = 0

        self.setCaption(i18n("Basket"))

        layout = QGridLayout(self, 1, 1, 11, 6)

        self.pkgLabel = QLabel(i18n("Selected packages:"), self)
        layout.addWidget(self.pkgLabel, 0, 0)

        self.pkgHBox = QHBox(self)
        layout.addMultiCellWidget(self.pkgHBox, 1, 1, 0, 2)

        self.extraLabel = QLabel(i18n("Extra Dependencies:"), self)
        layout.addWidget(self.extraLabel, 2, 0)

        self.depHBox = QHBox(self)
        layout.addMultiCellWidget(self.depHBox, 3, 3, 0, 2)

        self.totalSizeLabel = QLabel(i18n("Total Size:"), self)
        layout.addWidget(self.totalSizeLabel, 4, 0)

        spacer = QSpacerItem(121, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        layout.addItem(spacer, 5, 0)

        self.updateBasketButton = QPushButton(self)
        self.updateBasketButton.setText(i18n("Update Basket"))
        self.updateBasketButton.setIconSet(loadIconSet("package"))
        layout.addWidget(self.updateBasketButton, 5, 1)

        self.applyButton = QPushButton(self)
        self.applyButton.setText(parent.operateAction.text())
        self.applyButton.setIconSet(parent.operateAction.iconSet())
        layout.addWidget(self.applyButton, 5, 2)
        self.applyButton.setEnabled(False)

        self.connect(self.updateBasketButton, SIGNAL('clicked()'), self.updateBasket)
        self.connect(self.applyButton, SIGNAL('clicked()'), self.applyOperation)

        self.resize(QSize(574,503).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        # Read Css
        cssFile = file(str(locate("data","package-manager/layout.css"))).read()
        self.css = cssFile

        self.javascript = file(str(locate("data","package-manager/animation.js"))).read()

        self.pkgHtmlPart = KHTMLPart(self.pkgHBox)
        self.depHtmlPart = KHTMLPart(self.depHBox)

        self.createSelectedPackagesList()
        self.createExtraPackagesList()

        self.connect(self.pkgHtmlPart,SIGNAL("completed()"), self.registerEventListener)

    def updateBasket(self):
        print "update basket"
        QDialog.close(self, True)

    def applyOperation(self):
        print "apply"
        QDialog.close(self, True)

    def registerEventListener(self):
        self.eventListener = SelectEventListener(self)
        node = self.pkgHtmlPart.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

    def updateTotals(self):
        self.createExtraPackagesList()

    def createSelectedPackagesList(self):
        self.createHTML(self.packages, self.pkgHtmlPart, True)

    def createExtraPackagesList(self):
        self.totalSize = 0
        pkgs = self.packages
        if self.state == install_state:
            allPackages = pisi.api.generate_install_order(pkgs)
        elif self.state == remove_state:
            allPackages = pisi.api.generate_remove_order(pkgs)
        elif self.state == upgrade_state:
            allPackages = pisi.api.generate_upgrade_order(pkgs)

        extraPackages = list(set(allPackages) - set(pkgs))
        
        if extraPackages:
            self.extraLabel.show()
            self.depHBox.show()
            self.createHTML(extraPackages, self.depHtmlPart, False)
        else:
            self.extraLabel.hide()
            self.depHBox.hide()

        for package in allPackages:
             pkg = pisi.context.packagedb.get_package(package)
             self.totalSize += pkg.packageSize

        tpl = pisi.util.human_readable_size(self.totalSize)
        size = "%.0f %s" % (tpl[0], tpl[1])
        self.totalSizeLabel.setText(i18n("Total Size: %1").arg(size))

    def createHTML(self, packages, part=None, checkBox=False):
        head =  '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        '''

        if not part:
            part = self.htmlPart

        part.begin()
        part.write(head)
        part.write("<style type=\"text/css\">%s</style>" % self.css)
        part.write("<script language=\"JavaScript\">%s</script>" % self.javascript)
        part.write("</head><body>")
        part.write(self.createHTMLForPackages(packages, checkBox))
        part.write('''<body></html>''')
        part.end()

    def createHTMLForPackages(self, packages, checkBox):
        result = ''
        template ='''
        <!-- package start -->
        <div class="disabled">
        '''
        if checkBox:
            template += '''<div class="checkboks" style="%s"><input type="checkbox" checked name="%s"></div>'''

        template += '''
        <div class="package_title_disabled" style="%s">
        <img src="%s" style="float:left;" width="48px" height="48px">
        <b>%s</b><br>%s%s<br>%s<br>
        </div></div>
        <!-- package end -->
        '''

        style = "background-color:%s" % KGlobalSettings.baseColor().name()
        packages.sort(key=string.lower)

        for app in packages:
            package = pisi.context.packagedb.get_package(app)
            tpl = pisi.util.human_readable_size(package.packageSize)
            size = "%.0f %s" % (tpl[0], tpl[1])
            iconPath = getIconPath(package.icon)
            summary = package.summary
            if checkBox:
                result += template % (style,app,style,iconPath,app,i18n("Size: "),size,summary)
            else:
                result += template % (style,iconPath,app,i18n("Size: "),size,summary)

        return result

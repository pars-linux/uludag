# -*- coding: utf-8 -*-

from qt import *
from kdeui import *
from kdecore import KURL, KGlobal, KIcon, i18n

from pisi import specfile as spec

from pakito.gui.pspecWidget.sourceWidget import sourceWidget
from pakito.gui.pspecWidget.packageWidget import packageWidget
from pakito.gui.pspecWidget.historyWidget import historyWidget
from pakito.gui.editors import Editor as ed

from pakito.xmlUtil import XmlUtil

class PspecWidget(QWidget):
    """ a widget consists code and design view of an pspec.xml file """
    
    def __init__(self, parent, fileLocation):
        QWidget.__init__(self, parent)
        self.pspec = spec.SpecFile()
        self.fileLocation = fileLocation
        
        self.xmlUtil = XmlUtil(fileLocation)
        self.pspec.read(self.fileLocation)

        # code and design buttons
        self.pbDesign = KPushButton(i18n("Design"), self)
        self.pbDesign.setToggleButton(True)
        self.pbDesign.setOn(True)
        self.pbDesign.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.pbCode = KPushButton(i18n("Code"), self)
        self.pbCode.setToggleButton(True)
        self.pbCode.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # top of the widget - buttons and spacer
        mainLayout = QVBoxLayout(self, 5, 5)
        topLayout = QHBoxLayout(mainLayout)
        topLayout.addWidget(self.pbDesign)
        topLayout.addWidget(self.pbCode)
        topSpacer = QSpacerItem(200,20, QSizePolicy.Expanding)
        topLayout.addItem(topSpacer)
        
        # a widget stack controlled by "design" and "code" buttons
        self.widgetStack = QWidgetStack(self)
        mainLayout.addWidget(self.widgetStack)
        
        # toolbox of "source", "package(s)" and history
        self.toolBox = QToolBox(self.widgetStack)  
        self.toolBox.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        
        # source section of toolbox
        self.sourcePage = sourceWidget(self.toolBox, self.fileLocation, self.xmlUtil)
        
        # packages section of toolbox
        self.packagePage = packageWidget(self.toolBox, self.fileLocation, self.xmlUtil)
        
        # history section of toolbox
        self.historyPage = historyWidget(self.toolBox)
                
        # inclusion to toolbox
        self.toolBox.addItem(self.sourcePage, i18n("Source"))
        self.toolBox.addItem(self.packagePage, i18n("Package(s)"))
        self.toolBox.addItem(self.historyPage, i18n("History"))
        
        self.widgetStack.addWidget(self.toolBox, 0)
        self.editor = ed("xml", self.widgetStack)
        self.widgetStack.addWidget(self.editor, 1)
        
        # connections        
        self.connect(self.pbDesign, SIGNAL("clicked()"), self.pbDesignClicked)
        self.connect(self.pbCode, SIGNAL("clicked()"), self.pbCodeClicked)
        
        self.changeCount = 0
        self.change = False
        
        if self.fileLocation != None:
            self.fill()
        
    def where(self):
        if self.widgetStack.visibleWidget() is self.editor:
            return "code"
        else:
            return "design"
        
    def fill(self):
        #source bilgileri
        self.sourcePage.fill(self.pspec.source)
        
        # paket bilgileri
        self.packagePage.fill(self.pspec.packages)
        
        #history bilgileri
        self.historyPage.fill(self.pspec.history)
    
    def pbDesignClicked(self):
        if self.pbDesign.isOn(): # design section will open
            self.designWillOpen()
        else:
            self.codeWillOpen()
            
    def pbCodeClicked(self):
        if self.pbCode.isOn(): #code section will open
            self.codeWillOpen()            
        else:
            self.designWillOpen()
            
    def designWillOpen(self):
        qApp.setOverrideCursor(KCursor.workingCursor())
        res = self.syncFromCode()
        qApp.setOverrideCursor(KCursor.arrowCursor)

        if not res:
            KMessageBox.sorry(self, i18n("Specification is not valid or well-formed."), i18n("Invalid XML Code"))
            self.pbDesign.setOn(False)
            self.pbCode.setOn(True)
        else:
            qApp.setOverrideCursor(KCursor.workingCursor())
            self.fill()
            self.widgetStack.raiseWidget(0)
            self.pbCode.setOn(False)
            self.pbDesign.setOn(True)
            qApp.setOverrideCursor(KCursor.arrowCursor)

            
    def codeWillOpen(self):
        qApp.setOverrideCursor(KCursor.workingCursor())
        self.pbDesign.setOn(False)
        self.pbCode.setOn(True)
        self.widgetStack.raiseWidget(1)

        self.syncFromDesign()
        self.editor.openFile(self.fileLocation)
        qApp.setOverrideCursor(KCursor.arrowCursor)
    
    def syncFromCode(self):
        self.editor.save()
        try:
            self.pspec.read(self.editor.editedFile)
        except:
            return False
        return True
    
    def syncFromDesign(self):
        self.xmlUtil.write()
        
    def isSourceDownloaded(self):
        import os.path as path
        
        file = str(self.sourcePage.sourceleURI.text())
        if file.strip() == "":
            return (False, None)
        package = path.basename(file)
        loc = "/var/cache/pisi/archives/%s" % package
        if path.exists(loc):
            return (True, loc)
        else:
            return (False, None)        

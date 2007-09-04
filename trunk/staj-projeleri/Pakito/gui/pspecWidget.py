# -*- coding: utf-8 -*-

from qt import *
from kdeui import *
from kdecore import KURL, KGlobal, KIcon, i18n

from pisi import specfile as spec
from pisi.dependency import Dependency
from pisi.conflict import Conflict
from pisi.replace import Replace

from pspecWgt.sourceWidget import sourceWidget
from pspecWgt.packageWidget import packageWidget
from pspecWgt.historyWidget import historyWidget

class PspecWidget(QWidget):
    """ a widget consists code and design view of an pspec.xml file """
    
    def __init__(self, parent, fileLocation = None):
        QWidget.__init__(self, parent)
        self.pspec = spec.SpecFile()
        self.fileLocation = fileLocation
        if self.fileLocation != None:
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
        self.sourcePage = sourceWidget(self.toolBox, self.fileLocation)
        
        # packages section of toolbox
        self.packagePage = packageWidget(self.toolBox, self.fileLocation)
        
        # history section of toolbox
        self.historyPage = historyWidget(self.toolBox)
                
        # inclusion to toolbox
        self.toolBox.addItem(self.sourcePage, i18n("Source"))
        self.toolBox.addItem(self.packagePage, i18n("Package(s)"))
        self.toolBox.addItem(self.historyPage, i18n("History"))
        
        from editors import Editor as ed
        
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
        
    def fill(self, fileLocation = None):
        if fileLocation != None:
            try:
                self.pspec.read(fileLocation)
            except:
                return False            
            
        #source bilgileri
        self.sourcePage.fill(self.pspec.source)
        
        # paket bilgileri
        self.packagePage.fill(self.pspec.packages)
        
        #history bilgileri
        self.historyPage.fill(self.pspec.history)
        
        return True
    
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

        if not self.syncFromCode():
            KMessageBox.sorry(self, i18n("Specification is not valid or well-formed."), i18n("Invalid XML Code"))
            self.pbDesign.setOn(False)
            self.pbCode.setOn(True)
            return
        else:
            self.widgetStack.raiseWidget(0)
            self.pbCode.setOn(False)
            self.pbDesign.setOn(True)
            
    def codeWillOpen(self):
        self.pbDesign.setOn(False)
        self.pbCode.setOn(True)
        self.widgetStack.raiseWidget(1)
#        self.editor.widget().setFocus()        

        self.syncFromDesign()
        
    def codeChanged(self):
        if self.changeCount == 0:
            self.changeCount += 1
            return
        
        if not self.change:
            self.change = True
            self.emit(PYSIGNAL("changeName"), (True,))
    
    def get(self): # bu verdiklerimi doldurun ivedi
        
        #source bilgileri
        self.sourcePage.get(self.pspec.source)
        
        # paket bilgileri
        self.packagePage.get(self.pspec.packages)
        
        #history bilgileri
        self.historyPage.get(self.pspec.history)
    
    def syncFromCode(self):
        self.editor.save()
        return self.fill(self.editor.editedFile)
           
    def syncFromDesign(self):        
        try:
            self.get()
        except Exception, err:
            KMessageBox.error(self, str(err), i18n("Error during syncronisation"))
            return
        
        editFile = self.fileLocation
        try:
            self.pspec.write(editFile)
        except Exception, err:
            KMessageBox.sorry(self, i18n(str(err)), i18n("Error"))
        self.editor.openFile(editFile)
        
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
        

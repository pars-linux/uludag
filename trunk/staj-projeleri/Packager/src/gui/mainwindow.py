# -*- coding: utf-8 -*-

# TODO: layout/margin gözden geçir
# TODO: i18n
# TODO: packager profiles
# TODO: pyqt - endswith/endsWith bug?
# TODO: import ebuild?

from qt import *
from kdeui import *
from kdecore import KShortcut
from kparts import KParts
from widgets import *

import os
import shutil
from threading import Thread

import pisi.api
from pisi.config import Options
import pisi.ui

class MainWindow(KParts.MainWindow):
    """ Main window of the application """
    def __init__(self, *args):
        KParts.MainWindow.__init__(self, *args)
        iconloader = KGlobal.iconLoader()
        mainIcon = iconloader.loadIcon("pisikga", KIcon.Desktop)
        self.setIcon(mainIcon)
        self.setFixedSize(1010, 705) # TODO: maximize window?
        self.mainWidget =  QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.pspecTab = None 
        self.actionsTab = None
        self.tempDir = None
        self.realDir = None
#        self.toolBar = QToolBar(self)
#        self.toolBar.setLabel("Build Operations")
	    
        # main area
        self.mainLayout = QHBoxLayout(self.mainWidget, 6, 11)
        self.mainSplitter = QSplitter(self.mainWidget)
        self.mainSplitter.setOrientation(Qt.Vertical)
        self.topSplitter = QSplitter(self.mainSplitter)
        self.topSplitter.setOrientation(Qt.Horizontal)
        self.mainLayout.addWidget(self.mainSplitter)
        
        # left tree
#        self.lvProjects = KListView(self.topSplitter)
#        self.lvProjects.setMaximumWidth(200)
#        self.lvProjects.addColumn("Projects")
#        self.lvProjects.ResizeMode(KListView.LastColumn)

        #right tabs
        self.twTabs = KTabWidget(self.topSplitter)
        self.addWelcome()
        
        # bottom output tabs
        self.twBottomTabs = KTabWidget(self.mainSplitter)
        self.twBottomTabs.setMaximumHeight(200)
        self.twBottomTabs.setTabPosition(QTabWidget.Bottom)
#        self.bottomTabWidget1 = QHBox(self.twBottomTabs)
#        self.lvBottomTab = KListView(self.bottomTabWidget1)
#        self.lvBottomTab.addColumn("Messages")
#        self.twBottomTabs.addTab(self.bottomTabWidget1, "IDE Output")
        self.bottomTabWidget2 = QHBox(self.twBottomTabs)
        self.teOutput = KTextEdit(self.bottomTabWidget2)
        self.teOutput.setReadOnly(True)
        self.twBottomTabs.addTab(self.bottomTabWidget2, "IDE Output")
        
        # actions
        
        # (standard) file actions
        self.actionNew = KStdAction.openNew(self.new, self.actionCollection())
        self.actionOpen = KStdAction.open(self.open, self.actionCollection())
        self.actionSave = KStdAction.save(self.save, self.actionCollection())
        self.actionSaveAll = KAction("Save All", "save_all", KShortcut(), self.saveAll, self.actionCollection())
        self.actionClose = KStdAction.close(self.closePacket, self.actionCollection())
        self.actionExit = KStdAction.quit(self.exit, self.actionCollection())

#        # build actions        
        self.actionFetch = KAction("Fetch", "khtml_kget", KShortcut(), self.fetchSlot, self.actionCollection())
        self.actionUnpack = KAction("Unpack", KShortcut(), self.unpackSlot, self.actionCollection())        
        self.actionSetup = KAction("Setup", "configure", KShortcut(), self.setupSlot, self.actionCollection())
        self.actionBuild = KAction("Build", "compfile", KShortcut(), self.buildSlot, self.actionCollection())
        self.actionInstall = KAction("Install", KShortcut(), self.installSlot, self.actionCollection())
        self.actionMakePackage = KAction("Make Package", "package", KShortcut(), self.makePackageSlot, self.actionCollection())
        
        #automation actions
        self.actionAddRelease = KAction("Add Release", "edit_add", KShortcut(), self.addReleaseSlot, self.actionCollection())
        self.actionValidatePspec = KAction("Validate Pspec File", "ok", KShortcut(), self.validatePspecSlot, self.actionCollection())
        self.actionCheckSHA1 = KAction("Check SHA1", KShortcut(), self.checkSHA1Slot, self.actionCollection())
        self.actionComputeSHA1 = KAction("Compute SHA1", "gear", KShortcut(), self.computeSHA1Slot, self.actionCollection())
        self.actionDetectType = KAction("Detect File Type", "filefind", KShortcut(), self.detectTypeSlot, self.actionCollection())
    
        # menubar popups
        self.popupFile = KPopupMenu(self)
        self.actionNew.plug(self.popupFile)
        self.popupFile.insertSeparator()
        self.actionOpen.plug(self.popupFile)
        self.actionSave.plug(self.popupFile)
        self.actionSaveAll.plug(self.popupFile)
        self.popupFile.insertSeparator()
        self.actionClose.plug(self.popupFile)
        self.actionExit.plug(self.popupFile)
        
        self.popupBuild = KPopupMenu(self)
        self.actionFetch.plug(self.popupBuild)
        self.actionUnpack.plug(self.popupBuild)
        self.actionSetup.plug(self.popupBuild)
        self.actionBuild.plug(self.popupBuild)
        self.actionInstall.plug(self.popupBuild)
        self.popupBuild.insertSeparator()
        self.actionMakePackage.plug(self.popupBuild)
        
        popupAuto = KPopupMenu(self)
        self.actionAddRelease.plug(popupAuto)
        self.actionValidatePspec.plug(popupAuto)
        self.actionCheckSHA1.plug(popupAuto)
        self.actionComputeSHA1.plug(popupAuto)
        self.actionDetectType.plug(popupAuto)
        
        self.menuBar().insertItem("File", self.popupFile) # insertion
        self.menuBar().insertItem("Build", self.popupBuild) # insertion
        self.menuBar().insertItem("Automation", popupAuto)
        self.menuBar().insertItem("Help", self.helpMenu())
        
        # toolbar operations
        toolbar = self.toolBar()
        toolbar.setIconText(KToolBar.IconTextBottom)
        toolbar.setLabel("Main toolbar")
        self.actionNew.plug(toolbar)
        self.actionOpen.plug(toolbar)
        self.actionSave.plug(toolbar)
        self.actionSaveAll.plug(toolbar)
        
        # build toolbar
#        buildToolbar = QToolBar(self)  
        #TODO: Yeni bir toolbar yarat: KToolBar! Rrrrr
        toolbar.insertLineSeparator(-1, -1)
        self.actionFetch.plug(toolbar)
        self.actionSetup.plug(toolbar)
        self.actionBuild.plug(toolbar)
        self.actionMakePackage.plug(toolbar)
                
        #automation toolbar
        toolbar.insertLineSeparator(-1, -1)
        self.actionAddRelease.plug(toolbar)
        self.actionValidatePspec.plug(toolbar)
        self.actionComputeSHA1.plug(toolbar)
        self.actionDetectType.plug(toolbar)
        
        self.disableOperations()
        
        #prepare pisi 
        self.ui = UI(self.teOutput)
        
        # database true çünkü build --setup için gerekli
        try:
            self.options = Options()
            # TODO: Catbox violation için workaround !
            self.options.ignore_sandbox = True

            pisi.api.init(database = True, options = self.options, ui = self.ui)
            
        except Exception, err:
            print "Error during PiSi initialization: %s" % str(err)
            self.exit()
            
        self.pisithread = None

    def prepareBuild(self):
        self.teOutput.clear()
        if self.pspecTab.where() == "design":
            self.pspecTab.syncFromDesign()
        else:
            self.pspecTab.editor.save()
        self.pisithread = PisiThread()
        self.pisithread.setDaemon(True)
        
    def disableOperations(self):
        self.actionFetch.setDisabled(True)
        self.actionUnpack.setDisabled(True)
        self.actionSetup.setDisabled(True)
        self.actionBuild.setDisabled(True)
        self.actionInstall.setDisabled(True)
        self.actionMakePackage.setDisabled(True)
        
        self.actionAddRelease.setDisabled(True)
        self.actionValidatePspec.setDisabled(True)
        self.actionCheckSHA1.setDisabled(True)
        self.actionComputeSHA1.setDisabled(True)
        self.actionDetectType.setDisabled(True)        
        
    def enableOperations(self):
        self.actionFetch.setEnabled(True)
        self.actionUnpack.setEnabled(True)
        self.actionSetup.setEnabled(True)
        self.actionBuild.setEnabled(True)
        self.actionInstall.setEnabled(True)
        self.actionMakePackage.setEnabled(True)
        
        self.actionAddRelease.setEnabled(True)
        self.actionValidatePspec.setEnabled(True)
        self.actionCheckSHA1.setEnabled(True)
        self.actionComputeSHA1.setEnabled(True)
        self.actionDetectType.setEnabled(True)
        
    def new(self):
        self.closePacket()
        
        tempDir = "/tmp/packager-%d/" % os.getpid()
        
        if not os.path.isdir(tempDir):
            os.mkdir(tempDir)
            
        tempDir += "newPackage"
        os.mkdir(tempDir)
        shutil.copyfile("pspec-template.xml", tempDir + "/pspec.xml")
        shutil.copyfile("actions-template.py", tempDir + "/actions.py")
        self.tempDir = tempDir
            
        #create tabs
        self.pspecTab = pspecWidget(self.twTabs, self.tempDir + "/pspec.xml")
        self.actionsTab = actionsWidget(self.twTabs, self.tempDir + "/actions.py")
        
#        self.createGUI()
        
        # do connections for text change event
        self.connect(self.actionsTab, PYSIGNAL("changeName"), self.changeActionsTab)
        self.connect(self.pspecTab, PYSIGNAL("changeName"), self.changePspecTab)

        self.twTabs.addTab(self.pspecTab, "Specification")
        self.twTabs.addTab(self.actionsTab, "Actions")
        self.twTabs.setCurrentPage(0)
        
        self.enableOperations()
        
    def open(self):
    
	    # ask for directory of package - TODO: değiştirmeli mi?
        fileDialog = QFileDialog(self, "dialog", True)
        fileDialog.setMode(QFileDialog.DirectoryOnly)
        fileDialog.setCaption("Select PiSi Source Package")
        if not fileDialog.exec_loop():
            return
        packageDir = str(fileDialog.selectedFile())
        
        try: 
            self.pspecFile = open(packageDir + "pspec.xml", "r") 
        except:
            QMessageBox.warning(self, "Error", "No pspec.xml found.", QMessageBox.Ok)
            return
        self.pspecFile.close()
        
        try: 
            self.actionspyFile = open(packageDir + "actions.py", "r")
        except:
            QMessageBox.warning(self, "Error", "No actions.py found.", QMessageBox.Ok)
            return
        self.actionspyFile.close()
        
        # cleaning
        self.closePacket()
        
        self.realDir = packageDir
        tempDir = "/tmp/packager-%d/" % os.getpid()
        
        if not os.path.isdir(tempDir):
            os.mkdir(tempDir)
        
        hede, packageName = os.path.split(packageDir[:-1])
        del hede
        self.tempDir = tempDir + packageName
        if os.path.isdir(self.tempDir):
            shutil.rmtree(self.tempDir)

        shutil.copytree(packageDir, self.tempDir)

        self.pspecTab = pspecWidget(self.twTabs, os.path.join(self.tempDir, "pspec.xml"))
        
        if self.pspecTab == None: 
            QMessageBox.critical(self, "Invalid file", "pspec.xml is not valid or well-formed.")
            return
        
        self.actionsTab = actionsWidget(self.twTabs, os.path.join(self.tempDir, "actions.py"))
        self.twTabs.addTab(self.pspecTab, "Specification")
        self.twTabs.addTab(self.actionsTab, "Actions")
        self.twTabs.setCurrentPage(0)
        
        #connections
        self.connect(self.actionsTab, PYSIGNAL("changeName"), self.changeActionsTab)
        self.connect(self.pspecTab, PYSIGNAL("changeName"), self.changePspecTab)     
        
        self.enableOperations()
    
    def save(self, all=False):
        if self.actionsTab == None or self.actionsTab == None:
            KMessageBox.sorry(self, "There is no package to save. Create or Open a package first.", "No package")
            return
        
        if self.realDir == None:
            fileDialog = QFileDialog(self, "dialog", True)
            fileDialog.setMode(QFileDialog.DirectoryOnly)
            fileDialog.setCaption("Select PiSi Source Package Directory")
            if not fileDialog.exec_loop():
                return
            self.realDir = unicode(fileDialog.selectedFile())
            
        if all == True:
            self.changePspecTab(False)        
            self.pspecTab.change = False
            self.changeActionsTab(False)
            self.actionsTab.change = False
            
            self.savePspec()
            self.saveActions()
            return
        
        if self.twTabs.currentPage() is self.pspecTab:
            self.changePspecTab(False)
            self.pspecTab.change = False
            # real save process
            self.savePspec()
            return
        
        if self.twTabs.currentPage() is self.actionsTab:
            self.changeActionsTab(False)        
            self.actionsTab.change = False
            # real save process
            self.saveActions()
            return
    
    def saveAll(self):
        self.save(all = True)
    
    def savePspec(self):
        if self.pspecTab.where() == "design":
            self.pspecTab.syncFromDesign()
        else:
            self.pspecTab.editor.save()
        shutil.copyfile(self.tempDir+"/pspec.xml", self.realDir+"/pspec.xml")
    
    def saveActions(self):
        self.actionsTab.editor.save()
        shutil.copyfile(self.tempDir+"/actions.py", self.realDir+"/actions.py")
        
    def exit(self):
        self.closePacket()
        
        if self.tempDir:
            dir, hede = os.path.split(self.tempDir)
            del hede
            if os.path.isdir(dir):
                shutil.rmtree(dir)
        pisi.api.finalize()
        self.close()
    
    def changeActionsTab(self, changed=True):
        cur = self.twTabs.tabLabel(self.actionsTab)
        if changed and cur[0] != "*":
            self.twTabs.setTabLabel(self.actionsTab, "*" + cur)
            return
        if not changed and cur[0] == "*":
            self.twTabs.setTabLabel(self.actionsTab, cur[1:])
            
    def changePspecTab(self, changed=True):
        cur = self.twTabs.tabLabel(self.pspecTab)
        if changed and cur[0] != "*":
            self.twTabs.setTabLabel(self.pspecTab, "*" + cur)
            return
        
        if not changed and cur[0] == "*":
            self.twTabs.setTabLabel(self.pspecTab, cur[1:])
            return
            
    def closePacket(self):
#        if self.actionsTab and self.pspecTab:
#            if self.actionsTab.change or self.pspecTab.change:
#                ans = KMessageBox.questionYesNoCancel(self, "Do you want to save changes?", "Save")
#                if ans == KMessageBox.Yes :
#                    pass #TODO: Real save
#                elif ans == KMessageBox.No:
#                    pass
#                else:
#                    return
        
        if self.tempDir and os.path.isdir(self.tempDir):
            shutil.rmtree(self.tempDir)
        
        cleanTabs(self.twTabs)
        self.disableOperations()
#        self.addWelcome()
        self.actionsTab = None
        self.pspecTab = None
        self.realDir = None
        
        self.teOutput.clear()
        
    def addWelcome(self):
#        self.twTabs.addTab(QLabel("Welcome!", self.twTabs), "Welcome") # TODO: Düzgün bir Hoş geldiniz ekranı
        pass
        
    def fetchSlot(self):        
        self.prepareBuild()
        self.pisithread.setup(self.tempDir + "/pspec.xml", "fetch", self.teOutput)
        self.pisithread.start()
        
    def unpackSlot(self):
        self.prepareBuild()
        self.pisithread.setup(self.tempDir + "/pspec.xml", "unpack", self.teOutput)
        self.pisithread.start()
    
    def setupSlot(self):
        self.prepareBuild()
        self.pisithread.setup(self.tempDir + "/pspec.xml", "setup", self.teOutput)
        self.pisithread.start()
    
    def buildSlot(self):
        self.prepareBuild()
        self.pisithread.setup(self.tempDir + "/pspec.xml", "build", self.teOutput)
        self.pisithread.start()
    
    def installSlot(self):
        self.prepareBuild()
        self.pisithread.setup(self.tempDir + "/pspec.xml", "install", self.teOutput)
        self.pisithread.start()
    
    def makePackageSlot(self):
        self.prepareBuild()
        self.pisithread.setup(self.tempDir + "/pspec.xml", "buidpackages", self.teOutput, self.realDir)
        self.pisithread.start()
    
    def addReleaseSlot(self):
        rel = str(int(self.pspecTab.pspec.history[0].release) + 1)
        dlg = newListViewDialog(self, ["Release", "Date", "Version", "Comment", "Name", "E-mail", "Type"], "Add Release", [rel, "Date", "Version", "Comment", "Name", "E-mail", "Type"])
        if dlg.exec_loop() == KDialog.Rejected:
            return
        
        res = dlg.getResults()
        if res == None:
            return
        
        update = spec.Update()
        update.release = res[0]
        update.date = res[1]
        update.version = res[2]
        update.comment = res[3]
        update.name = unicode(res[4])
        update.email = res[5]
        update.type = res[6]
        self.pspecTab.historyPage.addRelease(update, True)
        self.pspecTab.pspec.history.insert(0, update)
        if self.pspecTab.where() == "code":
            self.pspecTab.syncFromDesign() 
    
    def validatePspecSlot(self):
        if self.pspecTab.where() == "design":
            KMessageBox.information(self, "Pspec file is valid.", "Valid File")
            return
        
        if not self.pspecTab.syncFromCode():
            KMessageBox.sorry(self, "Pspec file is not valid.", "Invalid File")
        else:
            KMessageBox.information(self, "Pspec file is valid.", "Valid File")
    
    def checkSHA1Slot(self):
        down, loc = self.pspecTab.isSourceDownloaded()
        if not down:
            KMessageBox.information(self, "Please fetch the source first.")
            return
#            ans = KMessageBox.questionYesNo(self, "Source must be downloaded first. Do you want to download now?", "Hmm")
#            if ans == KMessageBox.No:
#                return
#            self.fetchSlot()
#            self.pisithread.join()
        
        old = str(self.pspecTab.sourcePage.sourceleSHA1.text())
        if old.strip() == "":
            KMessageBox.information(self, "SHA1 field must be entered for check.")
            return
        import sha
        
        temp = open(loc)
        new = sha.new(temp.read()).hexdigest()
        temp.close()
        
        if old != new:
            KMessageBox.information(self, "Current SHA1 (%s) is invalid.\n\nValid one is %s" % (old, new), "Invalid SHA1")
        else:
            KMessageBox.information(self, "Current SHA1 is valid.", "Valid SHA1")        

    
    def computeSHA1Slot(self):
        down, loc = self.pspecTab.isSourceDownloaded()
        if not down:
            KMessageBox.information(self, "Please fetch the source first.")
            return
#            ans = KMessageBox.questionYesNo(self, "Source must be downloaded first. Do you want to download now?", "Hmm")
#            if ans == KMessageBox.No:
#                return
#            self.fetchSlot()
#            self.pisithread.join()
        import sha
        
        temp = open(loc)
        new = sha.new(temp.read()).hexdigest()
        temp.close()
        
        KMessageBox.information(self, "SHA1 is %s.\n\nThis will be set as current SHA1." % new, "SHA1 computed")
        self.pspecTab.sourcePage.sourceleSHA1.setText(new)
        
    def detectTypeSlot(self):
        types = {"bzip2": "tarbz2", "gzip": "targz"}
        
        down, loc = self.pspecTab.isSourceDownloaded()
        if not down:
            KMessageBox.information(self, "Please fetch the source first.")
            return
#            ans = KMessageBox.questionYesNo(self, "Source must be downloaded first. Do you want to download now?", "Hmm")
#            if ans == KMessageBox.No:
#                return
#            self.fetchSlot()
#            self.pisithread.join()
        
        com = os.popen("file %s | cut -f 2 -d\" \"" % loc)
        type = com.read()
        com.close()
        
        KMessageBox.information(self, "File type is: \"%s\".\nThis will be set as the current file type." % types[type.strip()], "Type detected")
        self.pspecTab.sourcePage.sourceleType.setText(types[type.strip()])
    
class PisiThread(Thread):
    
    def run(self):
         from cgi import escape
         try:
             pisi.api.build_until(self.path, self.stage)
             self.output.append("\n=> <b>Succesfully finished.</b>\n\n")
         except Exception, inst:
             self.output.append("\n<font color=\"red\">*** Error: %s</font>\n\n" % unicode(escape(inst)))
             return
         del self.output
         
         if self.stage == "buildpackages":
             # TODO: .pisi'nin yerini belirle
             command = "mv %s %s" % (os.getcwd() + "/*.pisi",self.pisiTo) #boşlukları handle et!
             os.system(command)

    def setup(self, path, stage, output, pisiTo=None):
        self.path = path
        self.stage = stage
        self.output = output
        self.pisiTo = pisiTo
    
class UI(pisi.ui.UI):
    def __init__(self, out):
        pisi.ui.UI.__init__(self)
        self.out = out
        self.set_debug(True)
        self.out.setPaper(QBrush(QColor("white")))
        
    def display(self, msg, color="black"):
        from cgi import escape
        try:
            finalStr = "<font color=\"%s\">%s</font>" % (color, unicode(escape(msg)))
            self.out.append(finalStr)
#            print finalStr
        except:
            print msg
    
    def info(self, msg, verbose = False, noln = False):
        self.display(msg, "darkblue")
    
    def debug(self, msg):
        self.display("DEBUG: " + msg, "brown")
    
    def warning(self, msg):
        self.display(msg, "purple")
        
    def error(self, msg):
        self.display("!!! " + msg, "red")
    
    def action(self, msg):
        self.display(msg, "darkgreen")
    
    def confirm(self, msg):
        self.display(msg + " auto-confirmed.", "red")
        return True
# -*- coding: utf-8 -*-

# TODO: layout/margin gözden geçir
# TODO: i18n
# TODO: packager profiles
# TODO: pyqt - endswith/endsWith bug?
# TODO: import ebuild?

# PyKDE/PyQT imports
from qt import *

from kdeui import *
from kdecore import *
from kparts import KParts
from kfile import KFileDialog
from kutils import *
from kparts import createReadOnlyPart

# System imports
import os
import shutil
from threading import Thread
import fcntl

# PiSi imports
import pisi.api
from pisi.config import Options 
import pisi.ui
import pisi

from pakito.gui.pspecWidget.pspecWidget import PspecWidget
from pakito.gui.pspecWidget.dialogs.permissionDialog import PermissionDialog
from pakito.gui.actionsWidget import ActionsWidget
from pakito.gui.multitabwidget import MultiTabWidget
from pakito.gui.componentWidget import ComponentWidget
from pakito.gui.optionsDialog import OptionsDialog
import pakito.templates 
from pakito.config import Config


class MainWindow(KParts.MainWindow):
    """ Main window of the application """
    def __init__(self, *args):
        KParts.MainWindow.__init__(self, *args)

        iconloader = KGlobal.iconLoader()
        mainIcon = iconloader.loadIcon("pisikga", KIcon.Desktop)
        self.setIcon(mainIcon)
        self.pspecTab = None
        self.actionsTab = None
        self.tempDir = None
        self.realDir = None
        self.pisithread = None
        self.componentTab = None
        self.newTempDir=None
	
	self.fetchFlag = 0
	self.setupFlag = 0
	self.buildFlag = 0
       	self.makePackageFlag = 0

        # main area
        self.mainWidget = QSplitter(self)
        self.mainWidget.setOrientation(Qt.Vertical)
        self.mainWidget.setHandleWidth(4)
        self.setCentralWidget(self.mainWidget)

        #right tabs
        self.twTabs = KTabWidget(self.mainWidget)
        self.addWelcome()

        # bottom output tabs
        self.twBottomTabs = MultiTabWidget(self.mainWidget, pos = KMultiTabBar.Bottom)

        bottomLayout = QHBox()
        self.teOutput = KTextEdit(bottomLayout)
        self.teOutput.setReadOnly(True)
        self.teOutput.setPaper(QBrush(QColor("white")))
        self.twBottomTabs.addTab(bottomLayout, iconloader.loadIcon("info", KIcon.Desktop), 0, "PiSi Output")

        part = createReadOnlyPart ("libkonsolepart", self)
        self.twBottomTabs.addTab(part.widget(), iconloader.loadIcon("openterm", KIcon.Desktop), 1, "Console")
        self.connect(part, SIGNAL("destroyed()"), self.konsoleClosedSlot)

        self.doActions()
        self.disableOperations()

        # get a pipe for OutputTab<-> PiSi communication

        self.pipeReadEnd, self.pipeWriteEnd = os.pipe()
        fcntl.fcntl(self.pipeReadEnd, fcntl.F_SETFL, os.O_NONBLOCK) #make it non-blocking to use qsocketnotifier 
        self.sockNotifier = QSocketNotifier(self.pipeReadEnd, QSocketNotifier.Read, self)
        self.connect(self.sockNotifier, SIGNAL("activated(int)"), self.sockHandle)        

        self.connect(qApp, SIGNAL("shutDown()"), self.exit)

        #TODO: setup'ta kdedir'e konulcak, alttakine gerek kalmayacak
        self.setXMLFile(os.getcwd() + "/pakitoui.rc")
        self.createShellGUI()

        self.showMaximized()

    def sockHandle(self, socket):
        currentOut = unicode(os.read(socket, 1000)).replace("\n", "<br>")
        self.teOutput.setText(unicode(self.teOutput.text() + currentOut))
        #this is not teOutput.append because, stream isn't splitted by new lines

        # scroll down if necessary
        self.teOutput.setContentsPos(0, self.teOutput.contentsHeight())

    def prepareBuild(self):
        self.teOutput.clear()
        if self.pspecTab.where() == "design":
            self.pspecTab.syncFromDesign()
        else:
            self.pspecTab.editor.save()

    def activateSave(self):
	self.actionSave.setEnabled(True)
	
    def deactivateSave(self):
	self.actionSave.setEnabled(False)

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

        self.actionClose.setEnabled(False)
        self.actionSave.setEnabled(False)

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

        self.actionClose.setEnabled(True)
        self.actionSave.setEnabled(True)

    def new(self):
        import datetime
        self.closePacket()

        tempDir = "/tmp/packager-%d/" % os.getpid()

        if not os.path.isdir(tempDir):
            os.mkdir(tempDir)

	try:
	    conf = Config()
            conf.read()
        except Exception, err:
            KMessageBox.sorry(self, i18n("Config file is not configured"))

	if conf.packagerName == '' and conf.packagerEmail == '' :
	    KMessageBox.sorry(self, i18n("Packager information is not configured!"))
	    return

        tempDir += "newPackage"
        os.mkdir(tempDir)
        templateDict = {"package": "PackageName", "homepage": "http://www.pardus.org.tr", "partof": "Pardus",
                 "packagername": conf.packagerName, "packageremail": conf.packagerEmail,
                 "license": "GPL-2", "isa": "isA",
                 "summary": "Summary",
                 "archivetype": "targz", "archiveuri": "URI",
                 "archivesha1": "SHA1", "date": str(datetime.date.today()), "version": "1.0"}        

        self.tempDir = tempDir

        f = open(tempDir + "/pspec.xml", "w")
        f.write(pakito.templates.pspecTemplate % templateDict)
        f.close()
        f = open(tempDir + "/actions.py", "w")
        f.write(pakito.templates.actionspyTemplate % templateDict)
        f.close()

        #create tabs
        self.pspecTab = PspecWidget(self.twTabs, self.tempDir + "/pspec.xml")
        self.actionsTab = ActionsWidget(self.twTabs, self.tempDir + "/actions.py")

#        self.createGUI()

        self.twTabs.addTab(self.pspecTab, i18n("Specification"))
        self.twTabs.addTab(self.actionsTab, i18n("Actions"))
        self.twTabs.setCurrentPage(0)

        self.enableOperations()

    def open(self):
	packageDir = KFileDialog.getExistingDirectory(QString.null, self, i18n("Select PiSi Source Package"))

	
        if not packageDir or packageDir == "":
            return
        else:
            packageDir = unicode(packageDir) + "/"

        try: 
            pspecFile = open(packageDir + "pspec.xml", "r+")
        except:
            KMessageBox.sorry(self, i18n("No pspec.xml found."), i18n("Error"))
            return
        pspecFile.close()

        try: 
            actionspyFile = open(packageDir + "actions.py", "r+")
        except:
            KMessageBox.sorry(self, i18n("No actions.py found."), i18n("Error") )
            return
        actionspyFile.close()

        #component.xml control
        component = os.path.isfile(os.path.join(packageDir, "..", "component.xml"))
        if not component:
            KMessageBox.sorry(self, i18n("No component.xml found."), i18n("Error"))

        qApp.setOverrideCursor(KCursor.waitCursor())

        # cleaning
        self.closePacket()

        self.realDir = packageDir
        tempDir = "/tmp/packager-%d/" % os.getpid()

        if not os.path.isdir(tempDir):
            os.mkdir(tempDir)

        packageName = os.path.split(packageDir[:-1])[1]
        self.newTempDir = tempDir + packageName

        if os.path.isdir(self.newTempDir):
            shutil.rmtree(self.newTempDir)

        shutil.copytree(packageDir, self.newTempDir)
        qApp.processEvents()

        try:
            self.pspecTab = PspecWidget(self.twTabs, os.path.join(self.newTempDir, "pspec.xml"))
        except Exception, err:
            qApp.restoreOverrideCursor()
            KMessageBox.sorry(self, i18n("pspec.xml cannot be parsed: %s" % str(err)), i18n("Invalid File"))
            self.closePacket()
            return

        #if component:
        #    newdir=os.path.realpath("component.xml")
        #    shutil.copyfile(newdir,tempDir+"component.xml")

        self.actionsTab = ActionsWidget(self.twTabs, os.path.join(self.newTempDir, "actions.py"))
        #if component:
        #    self.componentTab = ComponentWidget(self.twTabs, os.path.join(tempDir, "component.xml"))

        self.tempDir = tempDir + packageName
        self.twTabs.addTab(self.pspecTab, i18n("Specification"))
        self.twTabs.addTab(self.actionsTab, i18n("Actions"))
        #if component:
        #    self.twTabs.addTab(self.componentTab, i18n("Component"))
        self.twTabs.setCurrentPage(0)

        #connections
#        self.connect(self.actionsTab, PYSIGNAL("changeName"), self.changeActionsTab)
#        self.connect(self.pspecTab, PYSIGNAL("changeName"), self.changePspecTab)

        self.enableOperations()
        qApp.restoreOverrideCursor()

        self.createGUI(self.pspecTab.editor.part)

#    def eventFilter(self, obj, ev):
#        try:
#            if obj == self.pspecTab.editor and ev.type() == QEvent.MouseButtonPress:
#                print "hedeeee"
#        except:
#            pass

    def save(self):
        if self.actionsTab == None or self.actionsTab == None:
            KMessageBox.sorry(self, i18n("There is no package to save. Create or Open a package first."), i18n("No package"))
            return

        if self.realDir == None:
            packageDir = KFileDialog.getExistingDirectory(QString.null, self, i18n("Select PiSi Source Package Directory"))
            if not packageDir or str(packageDir) == "":
                return

            self.realDir = unicode(packageDir)

        if all == True:
            self.changePspecTab(False)
            self.pspecTab.change = False
            self.changeActionsTab(False)
            self.actionsTab.change = False

        self.savePspec()
        self.saveActions()

	if self.realDir[-1] != "/":
		self.realDir += "/"

	QMessageBox.information(self,
                                "Files Saved",
                                "Following files are saved:\n"+self.realDir+"pspec.xml\n"+self.realDir+"actions.py")

	#After save deactivate Save button, after a key pressed activate Save button...
	#SI self.deactivateSave()
	#SI QObject.connect(self.actionSave, SIGNAL("clicked()"), self.activateSave)


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
        qApp.setOverrideCursor(KCursor.waitCursor())

        self.closePacket()
        if self.tempDir:
            dir = os.path.split(self.tempDir)[0]
            if os.path.isdir(dir):
                shutil.rmtree(dir)
        self.close()
        self.pisithread.start()
#    def changeActionsTab(self, changed=True):
#        cur = self.twTabs.tabLabel(self.actionsTab)
#        if changed and cur[0] != "*":
#            self.twTabs.setTabLabel(self.actionsTab, "*" + cur)
#            return
#        if not changed and cur[0] == "*":
#            self.twTabs.setTabLabel(self.actionsTab, cur[1:])
#
#    def changePspecTab(self, changed=True):
#        cur = self.twTabs.tabLabel(self.pspecTab)
#        if changed and cur[0] != "*":
#            self.twTabs.setTabLabel(self.pspecTab, "*" + cur)
#            return
#
#        if not changed and cur[0] == "*":
#            self.twTabs.setTabLabel(self.pspecTab, cur[1:])
#            return

    def closePacket(self):
#        if self.actionsTab and self.pspecTab:
#            if self.actionsTab.change or self.pspecTab.change:
#                ans = KMessageBox.questionYesNoCancel(self, "Do you want to save changes?", "Save")
#                if ans == KMessageBox.Yes :
#               .     pass #TODO: Real save
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

    def konsoleClosedSlot(self):
        self.twBottomTabs.removeTab(1) #this must take Name as argument

        #generate new konsole
        part = createReadOnlyPart ("libkonsolepart", self)
        iconloader = KGlobal.iconLoader()
        self.twBottomTabs.addTab(part.widget(), iconloader.loadIcon("openterm", KIcon.Desktop), 1, "Console")
        self.connect(part, SIGNAL("destroyed()"), self.konsoleClosedSlot)

    def fetchSlot(self):
	#from pakito.gui.pspecWidget.sourceWidget import sourceWidget
	#if sourceWidget.lePartOf.text() == '' :
	   # KMessageBox.sorry(self, i18n("\"PartOf\" section must be filled!"))
	  #  return

        self.prepareBuild()
        self.twBottomTabs.expandTab()
        self.pisithread = PisiThread(self.tempDir + "/pspec.xml", "fetch", self.pipeWriteEnd)
        self.pisithread.start()
        qApp.processEvents(QEventLoop.ExcludeUserInput)

	self.fetchFlag = 1
    def unpackSlot(self):
        self.prepareBuild()
        self.twBottomTabs.expandTab()
        self.pisithread = PisiThread(self.tempDir + "/pspec.xml", "unpack", self.pipeWriteEnd)    
        self.pisithread.start()
        qApp.processEvents(QEventLoop.ExcludeUserInput)

    def setupSlot(self):
	from cgi import escape
	ui = UI(self.pipeWriteEnd)
        self.prepareBuild()
        self.twBottomTabs.expandTab()
        self.pisithread = PisiThread(self.tempDir + "/pspec.xml", "setup", self.pipeWriteEnd)    
        qApp.processEvents(QEventLoop.ExcludeUserInput)
	ui.display("Setup Slot is starting.", "black")
	if self.fetchFlag == 0:
	    try:
	        ui.confirm("Fetch operation is ")
	        self.fetchSlot()
	        os.write(self.pipeWriteEnd, "<b>Fetch operation is </b>")
	        #TOFIX: "Thread already started." 
	    except Exception, inst:
                os.write(self.pipeWriteEnd, str(i18n("\n<font color=\"red\">*** Error: %s</font><br>\n\n")) % unicode(escape(str(inst))))
                return

        self.pisithread.start()
        qApp.processEvents(QEventLoop.ExcludeUserInput)
	os.write(self.pipeWriteEnd, "<b>Setup slot operation is</b>")
	self.setupFlag = 1

    def buildSlot(self):
	ui = UI(self.pipeWriteEnd)
        self.twBottomTabs.expandTab()
        self.prepareBuild()
        self.pisithread = PisiThread(self.tempDir + "/pspec.xml", "build", self.pipeWriteEnd)
	ui.display("Build Slot is starting.", "black")
	ui.confirm("Fetch operation is ")
	if self.fetchFlag == 0:
	    #try:
	        ui.confirm("Fetch operation is ")
	        self.fetchSlot()
	        os.write(self.pipeWriteEnd, "<b>Fetch operation is </b>")
	        #TOFIX: "Thread already started." 
	        self.fetchFlag = 1
	    #except Exception, inst:
                #os.write(self.pipeWriteEnd, str(i18n("\n<font color=\"red\">*** Error: %s</font><br>\n\n")) % unicode(escape(str(inst))))
                #return
	ui.confirm("Start operation is ")
	if self.setupFlag == 0:
	    #try:
	        ui.confirm("Setup Slot operation is ")
	        self.setupSlot()
	        os.write(self.pipeWriteEnd, "<b>Setup Slot operation is </b>")
	        #TOFIX: "Thread already started." 
	        self.fetchFlag = 1
	    #except Exception, inst:
                #os.write(self.pipeWriteEnd, str(i18n("\n<font color=\"red\">*** Error: %s</font><br>\n\n")) % unicode(escape(str(inst))))
                #return

        self.pisithread.start()
        qApp.processEvents(QEventLoop.ExcludeUserInput)
	self.buildFlag = 1

    def installSlot(self):
	ui = UI(self.pipeWriteEnd)
        self.prepareBuild()
        self.twBottomTabs.expandTab()
        self.pisithread = PisiThread(self.tempDir + "/pspec.xml", "install", self.pipeWriteEnd)
	ui.display("Install Slot is starting.", "black")
        self.pisithread.start()
	ui.confirm("Fetch operation is ")
	if self.fetchFlag == 0:
	    try:
	        ui.confirm("Fetch operation is ")
	        self.fetchSlot()
	        os.write(self.pipeWriteEnd, "<b>Fetch operation is </b>")
	        #TOFIX: "Thread already started." 
	        self.fetchFlag = 1
	    except Exception, inst:
                os.write(self.pipeWriteEnd, str(i18n("\n<font color=\"red\">*** Error: %s</font><br>\n\n")) % unicode(escape(str(inst))))
                return
	ui.confirm("Setup slot operation is ")
	if self.setupFlag == 0:
	    try:
	        ui.confirm("Setup Slot operation is ")
	        self.setupSlot()
	        os.write(self.pipeWriteEnd, "<b>Setup Slot operation is </b>")
	        #TOFIX: "Thread already started." 
	        self.fetchFlag = 1
	    except Exception, inst:
                os.write(self.pipeWriteEnd, str(i18n("\n<font color=\"red\">*** Error: %s</font><br>\n\n")) % unicode(escape(str(inst))))
                return
	ui.confirm("Building slot operation is ")
	if self.buildFlag == 0:
	    try:
	        ui.confirm("Buildinf Slot operation is ")
	        self.setupSlot()
	        os.write(self.pipeWriteEnd, "<b>Building Slot operation is </b>")
	        #TOFIX: "Thread already started." 
	        self.fetchFlag = 1
	    except Exception, inst:
                os.write(self.pipeWriteEnd, str(i18n("\n<font color=\"red\">*** Error: %s</font><br>\n\n")) % unicode(escape(str(inst))))
                return
        qApp.processEvents(QEventLoop.ExcludeUserInput)

    def makePackageSlot(self):
        self.prepareBuild()
        self.twBottomTabs.expandTab()
        self.pisithread = PisiThread(self.tempDir + "/pspec.xml", "buildpackages", self.pipeWriteEnd, self.realDir)    
        self.pisithread.start()
        qApp.processEvents(QEventLoop.ExcludeUserInput)

    def addReleaseSlot(self):
        self.pspecTab.historyPage.slotAddHistory()

    def validatePspecSlot(self):
        if self.pspecTab.where() == "design":
            self.pspecTab.syncFromDesign()
            try:
                self.pspecTab.pspec.read(self.pspecTab.fileLocation)
                KMessageBox.information(self, i18n("Pspec file is valid."), i18n("Valid File"))
            except Exception, err:
                KMessageBox.sorry(self, i18n("Pspec file is not valid: %s" % err), i18n("Invalid File"))
        else:
            try:
                self.pspecTab.syncFromCode()
                KMessageBox.information(self, i18n("Pspec file is valid."), i18n("Valid File"))
            except Exception, err:
                KMessageBox.sorry(self, i18n("Pspec file is not valid: %s" % err), i18n("Invalid File"))

    def checkSHA1Slot(self):
        loc = self.pspecTab.isSourceDownloaded()
        if not loc:
            KMessageBox.information(self, i18n("Please fetch the source first."))
            return
#            ans = KMessageBox.questionYesNo(self, "Source must be downloaded first. Do you want to download now?", "Hmm")
#            if ans == KMessageBox.No:
#                return
#            self.fetchSlot()
#            self.pisithread.join()

        old = str(self.pspecTab.sourcePage.leSHA1.text())
        if old.strip() == "":
            KMessageBox.information(self, i18n("SHA1 field must be entered for check."))
            return
        import sha

        temp = open(loc)
        # TODO: büyük dosyalar için new() + update()'ler şeklinde değiştir
        new = sha.new(temp.read()).hexdigest()
        temp.close()

        if old != new:
            KMessageBox.information(self, i18n("Current SHA1 (%s) is invalid.\n\nValid one is %s") % (old, new), i18n("Invalid SHA1"))
        else:
            KMessageBox.information(self, i18n("Current SHA1 is valid."), i18n("Valid SHA1"))


    def computeSHA1Slot(self):
        loc = self.pspecTab.isSourceDownloaded()
        if not loc:
            KMessageBox.information(self, i18n("Please fetch the source first."))
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

        KMessageBox.information(self, str(i18n("SHA1 is %s.\n\nThis will be set as current SHA1.")) % new, i18n("SHA1 computed"))
        self.pspecTab.sourcePage.leSHA1.setText(new)

    def detectTypeSlot(self):

        def guessTypeByExtension(filename):
            if filename.endswith(".tar.gz") or filename.endswith(".tgz"):
                return "targz"
            elif filename.endswith(".tar.bz2") or filename.endswith(".tbz2"):
                return "tarbz2"
            elif filename.endswith(".zip"):
                return "zip"
            elif filename.endswith(".tar.lzma"):
                return "tarlzma"
            elif filename.endswith(".tar"):
                return "tar"
            elif filename.endswith(".gzip"):
                return "gzip"
            else:
                return "binary"

        loc = self.pspecTab.isSourceDownloaded()
        if not loc:
            KMessageBox.information(self, i18n("Please fetch the source first."))
            return
#            ans = KMessageBox.questionYesNo(self, "Source must be downloaded first. Do you want to download now?", "Hmm")
#            if ans == KMessageBox.No:
#                return
#            self.fetchSlot()
#            self.pisithread.join()

        ext = guessTypeByExtension(loc)
        KMessageBox.information(self, str(i18n("File type is: \"%s\".\nThis will be set as the current file type.")) % ext, i18n("Type detected"))
        self.pspecTab.sourcePage.cbType.setCurrentText(ext)

    def slotSettings(self):
        from pakito.config import Config

        dia = OptionsDialog(self)
        conf = Config()
        conf.read()
        dia.leName.setText(conf.packagerName)
        dia.leEmail.setText(conf.packagerEmail)
        if dia.exec_loop() == KDialog.Accepted:
            conf.packagerName = dia.leName.text()
            conf.packagerEmail = dia.leEmail.text()
            conf.write()

    def slotConfigureKeys(self):
        KKeyDialog.configure(self.actionCollection())

    def doActions(self):
        # actions

        # (standard) file actions
        self.actionNew = KStdAction.openNew(self.new, self.actionCollection(), "actionNew")
        self.actionOpen = KStdAction.open(self.open, self.actionCollection(), "actionOpen")
        self.actionSave = KStdAction.save(self.save, self.actionCollection(), "actionSave")
        self.actionSave.setEnabled(False)
#        self.actionSaveAll = KAction(i18n("Save All"), "save_all", KShortcut(), self.saveAll, self.actionCollection())
        self.actionClose = KStdAction.close(self.closePacket, self.actionCollection(), "actionClose")
        self.actionClose.setEnabled(False)
        self.actionExit = KStdAction.quit(self.exit, self.actionCollection(), "actionExit")

        #settings actions
        KStdAction.keyBindings(self.slotConfigureKeys, self.actionCollection())
        self.actionSettings = KStdAction.preferences(self.slotSettings, self.actionCollection())

        # build actions        
        self.actionFetch = KAction(i18n("Fetch"), "khtml_kget", KShortcut(), self.fetchSlot, self.actionCollection(), "actionFetch")
        self.actionUnpack = KAction(i18n("Unpack"), KShortcut(), self.unpackSlot, self.actionCollection(), "actionUnpack")        
        self.actionSetup = KAction(i18n("Setup"), "configure", KShortcut(), self.setupSlot, self.actionCollection(), "actionSetup")
        self.actionBuild = KAction(i18n("Build"), "compfile", KShortcut(), self.buildSlot, self.actionCollection(), "actionBuild")
        self.actionInstall = KAction(i18n("Install"), KShortcut(), self.installSlot, self.actionCollection(), "actionInstall")
        self.actionMakePackage = KAction(i18n("Make Package"), "package", KShortcut(), self.makePackageSlot, self.actionCollection(), "actionMakePackage")

        #automation actions
        self.actionAddRelease = KAction(i18n("Add Release"), "edit_add", KShortcut(), self.addReleaseSlot, self.actionCollection(), "actionAddRelease")
        self.actionValidatePspec = KAction(i18n("Validate Pspec File"), "ok", KShortcut(), self.validatePspecSlot, self.actionCollection(), "actionValidatePspec")
        self.actionCheckSHA1 = KAction(i18n("Check SHA1"), KShortcut(), self.checkSHA1Slot, self.actionCollection(), "actionCheckSHA1")
        self.actionComputeSHA1 = KAction(i18n("Compute SHA1"), "gear", KShortcut(), self.computeSHA1Slot, self.actionCollection(), "actionComputeSHA1")
        self.actionDetectType = KAction(i18n("Detect File Type"), "filefind", KShortcut(), self.detectTypeSlot, self.actionCollection(), "actionDetectType")

class PisiThread(Thread):
    def __init__(self, path, stage, pipe, pisiTo=None):
        Thread.__init__(self)
        self.path = path
        self.stage = stage
        self.output = pipe
        self.pisiTo = pisiTo
        self.setDaemon(True)

    def run(self):
         from cgi import escape
	 ui = UI(self.output)
         try:
             self.initPisi()
             qApp.processEvents(QEventLoop.ExcludeUserInput)
	     pisi.api.build(self.path)
	     qApp.processEvents(QEventLoop.ExcludeUserInput)
             os.write(self.output, str(i18n("<b>successfully finished.</b><br>")))
         except Exception, inst:
             os.write(self.output, str(i18n("\n<font color=\"red\">*** Error: %s</font><br>\n\n")) % unicode(escape(str(inst))))
             return

         if self.stage == "buildpackages":
             # TODO: .pisi'nin yerini belirle
	     self.pisiTo = self.path
             command = "mv %s %s" % (str(os.getcwd() + "/*.pisi").replace(" ", "\ "), self.pisiTo.replace(" ", "\ "))
             os.system(command)

    def initPisi(self):
        ui = UI(self.output)
        #SI opts = Options()
	opts = pisi.config.Options()
        opts.debug = True
#        pisi.api.init(database = True, write = False, options = opts, ui = ui, stdout = self.output, stderr = self.output, signal_handling = False)
        #SI pisi.api.init(database = True, write = False, options = opts, ui = ui, stderr = self.output, signal_handling = False)

class UI(pisi.ui.UI):
    def __init__(self, out):
        pisi.ui.UI.__init__(self)
        self.out = out
        self.set_debug(True)

    def display(self, msg, color="black"):
        from cgi import escape
        finalStr = "<font color=\"%s\">%s</font><br>" % (color, unicode(escape(msg)))
        os.write(self.out, finalStr)

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
        self.display(msg + " auto-confirmed.", "green")
        return True

    def checkPermission(self):
        from pakito.config import Config
        permissionDia = PermissionDialog(self)
        conf = Config()
        conf.read()
	
        if permissionDia.exec_loop() == KDialog.Accepted:
            conf.rootPassword = permissionDia.pePassword.text()
	    if permissionDia.cbRemember.isChecked() :
            	conf.write()

    def display_progress(self, **kwargs):
#        self.display(str(kwargs), "darkgreen")
#        print kwargs
        #TODO: display a progress bar
        pass

def cleanTabs(tw):
        for i in range(tw.count()):
            page = tw.currentPage()
            tw.removePage(page)
            page.close()

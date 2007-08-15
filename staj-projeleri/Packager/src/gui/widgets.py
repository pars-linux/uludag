# -*- coding: utf-8 -*-

from qt import *
from kdeui import *

from pisi import specfile as spec
from pisi.dependency import Dependency
from pisi.conflict import Conflict

from kdecore import KURL, KGlobal, KIcon

#TODO: Paket haline getir bu modülü

class pspecWidget(QWidget):
    """ a widget consists code and design view of an pspec.xml file """
    
    def __init__(self, parent, fileLocation = None):
        QWidget.__init__(self, parent)
        self.pspec = spec.SpecFile()
        self.fileLocation = fileLocation
        if self.fileLocation != None:
            self.pspec.read(self.fileLocation)

        # code and design buttons
        self.btnDesign = KPushButton("Design", self)
        self.btnDesign.setToggleButton(True)
        self.btnDesign.setOn(True)
        self.btnDesign.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.btnCode = KPushButton("Code", self)
        self.btnCode.setToggleButton(True)    
        self.btnCode.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
        # top of the widget - buttons and spacer
        mainLayout = QVBoxLayout(self, 5, 5)
        topLayout = QHBoxLayout(mainLayout)
        topLayout.addWidget(self.btnDesign)
        topLayout.addWidget(self.btnCode)
        topSpacer = QSpacerItem(200,20, QSizePolicy.Expanding)
        topLayout.addItem(topSpacer)
        
        # a widget stack controlled by "design" and "code" buttons
        self.widgetStack = QWidgetStack(self)
        mainLayout.addWidget(self.widgetStack)
        
        # toolbox of "source", "package(s)" and history
        self.toolBox = QToolBox(self.widgetStack)  
        
        # source section of toolbox
        self.sourcePage = sourceWidget(self.toolBox)
        
        # packages section of toolbox
        self.packagePage = packageWidget(self.toolBox)
        
        # history section of toolbox
        self.historyPage = historyWidget(self.toolBox)
                
        # inclusion to toolbox
        self.toolBox.addItem(self.sourcePage, "Source")
        self.toolBox.addItem(self.packagePage, "Package(s)")
        self.toolBox.addItem(self.historyPage, "History")
        
        from editors import editor as ed
        
        self.widgetStack.addWidget(self.toolBox, 0)
        self.editor = ed("xml", self.widgetStack)
        self.widgetStack.addWidget(self.editor, 1)
        
        # connections        
        self.connect(self.btnDesign, SIGNAL("clicked()"), self.btnDesignClicked)
        self.connect(self.btnCode, SIGNAL("clicked()"), self.btnCodeClicked)
#        self.connect(self.tePspecCode, SIGNAL("textChanged()"), self.codeChanged)
        
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
    
    def btnDesignClicked(self):
        if self.btnDesign.isOn(): # design section will open
            self.designWillOpen()            
        else:
            self.codeWillOpen()
            
    def btnCodeClicked(self):
        if self.btnCode.isOn(): #code section will open
            self.codeWillOpen()            
        else:
            self.designWillOpen()
            
    def designWillOpen(self):

        if not self.syncFromCode():
            KMessageBox.sorry(self, "Specification is not valid or well-formed.", "Invalid XML Code")
            self.btnDesign.setOn(False)
            self.btnCode.setOn(True)
            return
        else:
            self.widgetStack.raiseWidget(0)
            self.btnCode.setOn(False)
            self.btnDesign.setOn(True)
            
    def codeWillOpen(self):
        self.btnDesign.setOn(False)
        self.btnCode.setOn(True)
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
        import os
        tempfile = open("/tmp/packager-template-" + str(os.getpid()), "w")
        tempfile.write(self.editor.getContent())
        tempfile.close()
        fillResult = self.fill("/tmp/packager-template-" + str(os.getpid()))
        os.unlink("/tmp/packager-template-" + str(os.getpid()))
        return fillResult
    
    def syncFromDesign(self):        
        try:
            self.get()
        except Exception, err:
            KMessageBox.error(self, str(err), "Error during syncronisation")
            return
        
        editFile = self.fileLocation
        self.pspec.write(editFile)
        self.editor.openFile(editFile)
        
        # code kısmının senkronlanması
#        if not self.change:
#            self.change = True
#            self.tePspecCode.setText(content)
#            self.change = False
#        else:
#            self.tePspecCode.setText(content)        
#            pass

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
        
class sourceWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.listviewHeight = 140
        self.pageLayout = QVBoxLayout(self, 7, -1)
        sourceGroupBox = QGroupBox("General", self)
        sourceGroupBox.setFlat(True)
        sourceGroupBox.setAlignment(Qt.AlignHCenter)
        sourceGroupBox.setColumnLayout(0, Qt.Vertical) # hayati!
        sourceGridLayout = QGridLayout(sourceGroupBox.layout(), 0, 0, 5)
        
        #general information
        sourcelblName = QLabel("Name:", sourceGroupBox)
        sourcelblHomepage = QLabel("Homepage:", sourceGroupBox)
        sourcelblLicense = QLabel("License:", sourceGroupBox)
        sourcelblIsA = QLabel("Is a:", sourceGroupBox)
        sourcelblPartOf = QLabel("Part of:", sourceGroupBox)
        sourcelblPackager = QLabel("Packager:", sourceGroupBox)
        self.sourceleName = KLineEdit(sourceGroupBox)
        self.sourceleHomepage = KLineEdit(sourceGroupBox)
        self.sourceleLicense = KLineEdit(sourceGroupBox)
        self.sourceleIsA = KLineEdit(sourceGroupBox)
#        self.sourcebtnAddIsA = KPushButton("+", sourceGroupBox)
#        self.sourcebtnAddIsA.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#        self.sourcebtnRemoveIsA = KPushButton("-", sourceGroupBox)
#        self.sourcebtnRemoveIsA.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sourcelePartOf = KLineEdit(sourceGroupBox)
        self.sourcecmbPackager = KLineEdit(sourceGroupBox)
        
        # inclusion to layout
        sourceGridLayout.addWidget(sourcelblName, 0, 0)
        sourceGridLayout.addWidget(self.sourceleName, 0, 1)
        sourceGridLayout.addWidget(sourcelblHomepage, 1, 0)
        sourceGridLayout.addWidget(self.sourceleHomepage, 1, 1)
        sourceGridLayout.addWidget(sourcelblLicense, 2, 0)
        sourceGridLayout.addWidget(self.sourceleLicense, 2, 1)
        sourceGridLayout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed), 0, 2)
        sourceGridLayout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed), 1, 2)
        sourceGridLayout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed), 2, 2)
        sourceGridLayout.addWidget(sourcelblIsA, 0, 3)
        sourceGridLayout.addWidget(sourcelblPartOf, 1, 3)
        sourceGridLayout.addWidget(sourcelblPackager, 2, 3)
        sourceGridLayout.addWidget(self.sourceleIsA, 0, 4)
#        sourceGridLayout.addWidget(self.sourcebtnAddIsA, 0, 5)
#        sourceGridLayout.addWidget(self.sourcebtnRemoveIsA, 0, 6)
        sourceGridLayout.addWidget(self.sourcelePartOf, 1, 4)
        sourceGridLayout.addWidget(self.sourcecmbPackager, 2, 4)
        
        # design of tabs about archive, summaries, deps and patches
        sourceTabWidget = KTabWidget(self)
        
        #archive section
        sourceArchiveWidget = QWidget(sourceTabWidget)
        sourceArchiveLayout = QGridLayout(sourceArchiveWidget, 0, 0, 5, 15)
        sourcelblURI = QLabel("URI:", sourceArchiveWidget)
        self.sourceleURI = KLineEdit(sourceArchiveWidget)
        sourcelblSHA1 = QLabel("SHA1:", sourceArchiveWidget)
        self.sourceleSHA1 = KLineEdit(sourceArchiveWidget)
        sourcelblType = QLabel("Type:", sourceArchiveWidget)
        self.sourceleType = KLineEdit(sourceArchiveWidget)
        sourceArchiveLayout.addWidget(sourcelblURI, 0, 0)
        sourceArchiveLayout.addWidget(self.sourceleURI, 0, 1)
        sourceArchiveLayout.addWidget(sourcelblSHA1, 1, 0)
        sourceArchiveLayout.addWidget(self.sourceleSHA1, 1, 1)
        sourceArchiveLayout.addWidget(sourcelblType, 2, 0)
        sourceArchiveLayout.addWidget(self.sourceleType, 2, 1)
        sourceTabWidget.addTab(sourceArchiveWidget, "Archive")
        
        #summary and desc. section
        self.sourceSummary = newListView(sourceTabWidget, ["Language", "Summary", "Description"], self.listviewHeight)
        sourceTabWidget.addTab(self.sourceSummary, "Summary & Description")
        
        #build deps. section
        self.sourceBuildDeps = newListView(sourceTabWidget, ["Condition", "Dependency"], self.listviewHeight)
        sourceTabWidget.addTab(self.sourceBuildDeps, "Build Dependencies")
        
        #patches section
        self.sourcePatches = newListView(sourceTabWidget, ["Level", "Patch"], self.listviewHeight)
        sourceTabWidget.addTab(self.sourcePatches, "Patches")
        
        # inclusion of general info. and other tabs
        self.pageLayout.addWidget(sourceGroupBox)
        self.pageLayout.addWidget(sourceTabWidget)  
        
#        self.connect(self.sourcecbPartOf, SIGNAL("toggled(bool)"), self.sourcecmbPartOf.setEnabled)  
        
    def fill(self, source):
        self.sourceleName.setText(source.name)
        self.sourceleHomepage.setText(source.homepage)
        self.sourceleLicense.setText(", ".join(source.license))
        self.sourceleIsA.setText(", ".join(source.isA))
#        self.sourcecmbPackager.insertItem("%s (%s)" % (source.packager.name, source.packager.email))
        self.sourcecmbPackager.setText("%s (%s)" % (source.packager.name, source.packager.email))
        if source.partOf:
            self.sourcelePartOf.setText(source.partOf)   
        
        #archive
        self.sourceleURI.setText(source.archive.uri)
        self.sourceleType.setText(source.archive.type)
        self.sourceleSHA1.setText(source.archive.sha1sum)

        self.sourceSummary.listView.clear()
        for lang, sum in source.summary.iteritems(): #TODO: summary yok desc varsa?
            lvi = KListViewItem(self.sourceSummary.listView, lang, unicode(sum))
            if lang in source.description:
                lvi.setText(2, unicode(source.description[lang]))

        self.sourceBuildDeps.listView.clear()
#        source.buildDependencies.reverse()
        for dep in source.buildDependencies:
            lvi = KListViewItem(self.sourceBuildDeps.listView, getConstraint(dep), dep.package)
        
        self.sourcePatches.listView.clear()
#        source.patches.reverse()
        for patch in source.patches:
            if not patch.level:
                patch.level = ""
            lvi = KListViewItem(self.sourcePatches.listView, str(patch.level), patch.filename)
    
    def get(self, source):
        if str(self.sourceleName.text()).strip() == "":
            raise Exception, "Source name must be filled"
        
        source.name = str(self.sourceleName.text()).strip()
        source.homepage = str(self.sourceleHomepage.text()).strip()
        source.license = str(self.sourceleLicense.text()).strip().split(", ")
        source.isA = str(self.sourceleIsA.text()).strip().split(", ")
        if self.sourcelePartOf.text() and str(self.sourcelePartOf.text()).strip() != "":
            source.partOf = str(self.sourcelePartOf.text()).strip()
        else:
            source.partOf = None
        
        packagerText = str(self.sourcecmbPackager.text()).strip()
        if packagerText != "":
            packager = packagerText.split(" (")
            packagerName = unicode(packager[0])
            packagerEmail = packager[1][:-1]
            source.packager.name = packagerName
            source.packager.email = packagerEmail
        else:
            pass # hata
        
        source.archive.uri= str(self.sourceleURI.text()).strip()
        source.archive.type = str(self.sourceleType.text()).strip()
        source.archive.sha1sum = str(self.sourceleSHA1.text()).strip()
        
        source.summary.clear()
        source.description.clear()
        iterator = QListViewItemIterator(self.sourceSummary.listView)
        while iterator.current():
            lvi = iterator.current()
            if str(lvi.text(1)).strip() != "":
                source.summary[str(lvi.text(0))] = unicode(lvi.text(1))
            if str(lvi.text(2)).strip() != "":
                source.description[str(lvi.text(0))] = unicode(lvi.text(2))
            iterator += 1
            
        source.buildDependencies = []
        iterator = QListViewItemIterator(self.sourceBuildDeps.listView)
        while iterator.current():
            lvi = iterator.current()
            dep = Dependency()
            getConstraintReverse(str(lvi.text(0)), str(lvi.text(1)), dep)
            source.buildDependencies.insert(0,dep)
            iterator += 1
        
        source.patches = []
        iterator = QListViewItemIterator(self.sourcePatches.listView)
        while iterator.current():
            lvi = iterator.current()
            patch = spec.Patch()
            if str(lvi.text(0)) == "":
                patch.level = None
            else:
                patch.level = int(str(lvi.text(0)))
            
            patch.filename = str(lvi.text(1))
            source.patches.insert(0,patch)
            iterator += 1
    
class packageWidget(QWidget):
    
    class packageTab(QWidget):
        def __init__(self, parent):
            QWidget.__init__(self, parent)
            self.listviewHeight = 140
            self.pageLayout = QVBoxLayout(self, 7, -1)
            groupBox = QGroupBox("General", self)
            groupBox.setFlat(True)
            groupBox.setAlignment(Qt.AlignHCenter)
            groupBox.setColumnLayout(0, Qt.Vertical) # hayati!
            gridLayout = QGridLayout(groupBox.layout(), 0, 0, 5)
            
            #general information
            lblName = QLabel("Name:", groupBox)
            lblLicense = QLabel("License:", groupBox)
            lblIsA = QLabel("Is a:", groupBox)
            lblPartOf = QLabel("Part of:", groupBox)
            self.leName = KLineEdit(groupBox)
            self.leLicense = KLineEdit(groupBox)
            self.leIsA = KLineEdit(groupBox)
#            self.btnAddIsA = KPushButton("+", groupBox)
#            self.btnAddIsA.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#            self.btnRemoveIsA = KPushButton("-", groupBox)
#            self.btnRemoveIsA.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.lePartOf = KLineEdit(groupBox)
#            self.cmbPartOf.setDisabled(True)
            
            # inclusion to layout
            gridLayout.addWidget(lblName, 0, 0)
            gridLayout.addWidget(self.leName, 0, 1)
            gridLayout.addWidget(lblLicense, 1, 0)
            gridLayout.addWidget(self.leLicense, 1, 1)
            gridLayout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed), 0, 2)
            gridLayout.addItem(QSpacerItem(10, 10, QSizePolicy.Fixed), 1, 2)
            gridLayout.addWidget(lblIsA, 0, 3)
            gridLayout.addWidget(self.leIsA , 0, 4)
#            gridLayout.addWidget(self.btnAddIsA, 0, 5)
#            gridLayout.addWidget(self.btnRemoveIsA, 0, 6)
            gridLayout.addWidget(lblPartOf, 1, 3)
            gridLayout.addWidget(self.lePartOf, 1, 4)
            
            # design of tabs about archive, summaries, deps and patches
            TabWidget = KTabWidget(self)
            
            #summary and desc. section
            self.summary = newListView(TabWidget, ["Language", "Summary", "Description"], self.listviewHeight)
            TabWidget.addTab(self.summary, "Summary & Description")
            
            #runtime deps. section
            self.runtimeDeps = newListView(TabWidget, ["Condition", "Dependency"], self.listviewHeight)
            TabWidget.addTab(self.runtimeDeps, "Runtime Dependencies")
            
            #files section
            self.files = newListView(TabWidget, ["Type", "Permanent?", "Path"], self.listviewHeight)
            TabWidget.addTab(self.files, "Files")
            
            #additional files section
            self.addFiles = newListView(TabWidget, ["Owner", "Permission", "Target", "File"], self.listviewHeight)
            TabWidget.addTab(self.addFiles, "Additional Files")
            
            #Conflicts section
            self.conflicts = newListView(TabWidget, ["Condition", "Package"], self.listviewHeight)
            TabWidget.addTab(self.conflicts, "Conflicts")
            
            #COMAR Scripts section
            self.comar = newListView(TabWidget, ["Provides", "Script"], self.listviewHeight)
            TabWidget.addTab(self.comar, "COMAR Scripts")
            
            # inclusion of general info. and other tabs
            self.pageLayout.addWidget(groupBox)
            self.pageLayout.addWidget(TabWidget)  
            
#            self.connect(self.cbPartOf, SIGNAL("toggled(bool)"), self.cmbPartOf.setEnabled)  
        
        def fill(self, package):
            # general info
            self.leName.setText(package.name)
            self.leLicense.setText(", ".join(package.license))
            self.leIsA.setText(", ".join(package.isA))
            if package.partOf:
#                self.cbPartOf.setChecked(True)
#                self.cmbPartOf.insertItem(package.partOf)
                self.lePartOf.setText(package.partOf)
                
            # summary and descriptions
            self.summary.listView.clear()
            for lang, sum in package.summary.iteritems(): #TODO: summary yok desc varsa?
                lvi = KListViewItem(self.summary.listView, lang, unicode(sum))
                if lang in package.description:
                    lvi.setText(2, unicode(package.description[lang]))
            
            #runtime deps.
            self.runtimeDeps.listView.clear()
            runDeps = package.runtimeDependencies()
#            runDeps.reverse()
            for dep in runDeps:
                lvi = KListViewItem(self.runtimeDeps.listView, getConstraint(dep), dep.package)
                
            # files
            self.files.listView.clear()
#            package.files.reverse()
            for file in package.files:  
                if not file.permanent:
                    file.permanent = ""
                lvi = KListViewItem(self.files.listView, file.fileType, file.permanent, file.path)                
                
            # additional files
            self.addFiles.listView.clear()
#            package.additionalFiles.reverse()
            for file in package.additionalFiles:  
                lvi = KListViewItem(self.addFiles.listView, file.owner, file.permission, file.target, file.filename)  
                
            # conflicts
            self.conflicts.listView.clear()
#            package.conflicts.reverse()
            for conf in package.conflicts:  
                lvi = KListViewItem(self.conflicts.listView, getConstraint(conf), conf.package)  
                
            # COMAR 
            self.comar.listView.clear()
#            package.providesComar.reverse()
            for comar in package.providesComar:  #TODO: summary yok desc varsa?
                lvi = KListViewItem(self.comar.listView, comar.om, comar.script) 
                 
        def get(self, package):
            if str(self.leName.text()):
                package.name = str(self.leName.text())
            if str(self.leLicense.text()):
                package.license = str(self.leLicense.text()).split(", ")
            else:
                package.license = None
            if str(self.leIsA.text()):
                package.isA = str(self.leIsA.text()).split(", ")
            else:
                package.isA = None
            if self.lePartOf.text() and str(self.lePartOf.text()).strip() != "":
                package.partOf = str(self.lePartOf.text())
            else:
                package.partOf = None
    
    	    #get package summary and desc.
            package.summary.clear()
            package.description.clear()
            iterator = QListViewItemIterator(self.summary.listView)
            while iterator.current():
                lvi = iterator.current()
                if str(lvi.text(1)).strip() != "":
                    package.summary[str(lvi.text(0))] = unicode(lvi.text(1))
                if str(lvi.text(2)).strip() != "":
                    package.description[str(lvi.text(0))] = unicode(lvi.text(2))
                iterator += 1
                
            #get package runtime dependencies
            # TODO: componentDependencies
            package.packageDependencies = []
            iterator = QListViewItemIterator(self.runtimeDeps.listView)
            while iterator.current():
                lvi = iterator.current()
                dep = Dependency()
                getConstraintReverse(str(lvi.text(0)), str(lvi.text(1)), dep)
                package.packageDependencies.insert(0,dep)
                iterator += 1
            
            #get package files
            package.files = []
            iterator = QListViewItemIterator(self.files.listView)
            while iterator.current():
                lvi = iterator.current()
                path = spec.Path()
                path.fileType = str(lvi.text(0))
                if str(lvi.text(1)).strip() != "":
                    path.permanent = str(lvi.text(1))
                path.path = str(lvi.text(2))
                package.files.insert(0,path)
                iterator += 1            
            
            #get package additional files
            package.additionalFiles = []
            iterator = QListViewItemIterator(self.addFiles.listView)
            while iterator.current():
                lvi = iterator.current()
                addFile = spec.AdditionalFile()
                if str(lvi.text(0)).strip() != "":
                    addFile.owner = str(lvi.text(0))
                if str(lvi.text(1)).strip() != "":
                    addFile.permission = str(lvi.text(1))
                if str(lvi.text(2)).strip() != "":
                    addFile.target = str(lvi.text(2))
                addFile.filename = str(lvi.text(3))                
                package.additionalFiles.insert(0,addFile)
                iterator += 1    
        
            #get package conflicts
            package.conflicts = []
            iterator = QListViewItemIterator(self.conflicts.listView)
            while iterator.current():
                lvi = iterator.current()
                conflict = Conflict()
                getConstraintReverse(str(lvi.text(0)), str(lvi.text(1)), conflict)
                package.conflicts.insert(0,conflict)
                iterator += 1 
        
            #get comar scripts
            package.providesComar = []
            iterator = QListViewItemIterator(self.comar.listView)
            while iterator.current():
                lvi = iterator.current()
                comar = spec.ComarProvide()
                if str(lvi.text(0)).strip() != "":
                    comar.om = str(lvi.text(0))
                if str(lvi.text(1)).strip() != "":
                    comar.script = str(lvi.text(1))               
                package.providesComar.insert(0,comar)
                iterator += 1    
		
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        pageLayout = QVBoxLayout(self, 6, 11)
        topLayout = QHBoxLayout(pageLayout, 5)
        
        # add/remove package buttons
        btnAddPackage = KPushButton("Add New Package", self)
        btnRemovePackage = KPushButton("Remove Package", self)
        topSpacer = QSpacerItem(250, 20, QSizePolicy.Expanding)
        topLayout.addWidget(btnAddPackage)
        topLayout.addWidget(btnRemovePackage)
        topLayout.addItem(topSpacer)
        
        self.twPackages = KTabWidget(self)
        pageLayout.addWidget(self.twPackages)
        
        self.connect(btnAddPackage, SIGNAL("clicked()"), self.addPackageSlot)
        self.connect(btnRemovePackage, SIGNAL("clicked()"), self.removePackageSlot)
    
    def addPackage(self, package, focus = False):
        tab = self.packageTab(self.twPackages)
        tab.fill(package)
        self.twPackages.addTab(tab, package.name)
        if focus:
            self.twPackages.showPage(tab)
    
    def fill(self, packages):
        # Add packages
        cleanTabs(self.twPackages)
        self.packages = packages
        for package in packages:
            self.addPackage(package)
            
    def get(self, packages):
        while len(packages) != 0:
            packages.pop()
        
        packageCount = self.twPackages.count()        
        for i in range(packageCount):
            tab = self.twPackages.page(i)
            package = spec.Package()
            #sen de bunu doldur heman
            tab.get(package)
            packages.append(package)
    
    def addPackageSlot(self):
        package = spec.Package()
        package.name = "NewPackage"
        fil = spec.Path()
        fil.fileType = "fileType"
        fil.path = "/path"
        package.files = []
        package.files.append(fil)
        self.addPackage(package, focus = True)
    
    def removePackageSlot(self):
        if self.twPackages.count() == 1:
            KMessageBox.error(self, "At least one package must exist.", "Error")
            return
        self.twPackages.removePage(self.twPackages.currentPage())
        
class historyWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.pageLayout = QHBoxLayout(self)
        
        self.history = newListView(self, ["Release", "Date", "Version", "Comment", "Name", "E-mail", "Type"])
        self.pageLayout.addWidget(self.history)
        
    def addRelease(self, rel, reverse=False):
        if not rel.type:
            rel.type = ""
        lvi = KListViewItem(self.history.listView, rel.release, 
                                rel.date, rel.version, 
                                rel.comment, rel.name, 
                                rel.email, rel.type)
        if reverse:
            lvi.moveItem(self.history.listView.lastItem())
        
    def fill(self, history):
        self.history.listView.clear()
#        history.reverse() # 
        for rel in history:
            self.addRelease(rel)
    
    def get(self, history):
        while len(history) != 0:
            history.pop()
            
        iterator = QListViewItemIterator(self.history.listView)
#        iterator += self.historylv.childCount() - 1
        while iterator.current():
            lvi = iterator.current()
            update = spec.Update()
            if str(lvi.text(0)).strip() != "":
                update.release = str(lvi.text(0))
            if str(lvi.text(1)).strip() != "":
                update.date = str(lvi.text(1))
            if str(lvi.text(2)).strip() != "":
                update.version = str(lvi.text(2))     
            if str(lvi.text(3)).strip() != "":
                update.comment = str(lvi.text(3))
            if str(lvi.text(4)).strip() != "":
                update.name = unicode(lvi.text(4))
            if str(lvi.text(5)).strip() != "":
                update.email = str(lvi.text(5))        
            if str(lvi.text(6)).strip() != "":
                update.type = str(lvi.text(6))
            history.insert(0,update)
            iterator += 1    

class actionsWidget(QWidget):
    def __init__(self, parent, actionsFile = None):
        QWidget.__init__(self, parent)
        self.mainLayout = QVBoxLayout(self, 5, 5)
        self.mainLayout.setAutoAdd(True)
        self.change = False
        
        from editors import editor as ed
        self.editor = ed("python", self)
        
        if actionsFile != None:
            self.editor.openFile(actionsFile)
        
        # event connection
#        self.connect(self.teActions, SIGNAL("textChanged()"), self.changed)
        
    def changed(self):
        if not self.change:
            self.change = True
            self.emit(PYSIGNAL("changeName"), (True,))
        
    def fill(self, file):
        from os.path import abspath
        self.editor.openURL(KURL("file://%s" % abspath(file)))
        
def getConstraint(dep):
    if dep.version:
        constraint = "Version = " + dep.version
    elif dep.versionTo:
        constraint = "Version <= " + dep.versionTo
    elif dep.versionFrom:
        constraint = "Version >= " + dep.versionFrom
    elif dep.release:
        constraint = "Release = " + dep.release
    elif dep.releaseTo:
        constraint = "Release <= " + dep.releaseTo
    elif dep.releaseFrom:
        constraint = "Release >= " + dep.releaseFrom
    else:
        constraint = ""
    return constraint

def getConstraintReverse(condition, package, dep):
    dep.version = dep.versionFrom = dep.versionTo = None
    dep.release = dep.releaseFrom = dep.releaseTo = None
    
    if condition.startswith("Version = "):
        dep.version = condition.split("= ")[1]
    elif condition.startswith("Version <= "):
        dep.versionTo = condition.split("= ")[1]
    elif condition.startswith("Version >= "):
        dep.versionFrom = condition.split("= ")[1]
    elif condition.startswith("Release = "):
        dep.release = condition.split("= ")[1]
    elif condition.startswith("Release <= "):
        dep.releaseTo = condition.split("= ")[1]
    elif condition.startswith("Release >= "):
        dep.releaseFrom = condition.split("= ")[1]

    dep.package = package
    
def cleanTabs(tw):
        for i in range(tw.count()):
            page = tw.currentPage()
            tw.removePage(page)
            page.close()
    
class newListView(QWidget):
    def __init__(self, parent, columns, maxHeight = 0):
        QWidget.__init__(self, parent)
        self.columns = columns
        mainLayout = QHBoxLayout(self, 4, 4)
        iconloader = KGlobal.iconLoader()
        
        #setup the listview
        self.listView = KListView(self)
        self.listView.setAllColumnsShowFocus(True)
        self.listView.setSorting(-1)
        if maxHeight != 0:
            self.listView.setMaximumHeight(maxHeight)
        self.addColumns()
        self.listView.setResizeMode(KListView.LastColumn)
        mainLayout.addWidget(self.listView)
        
        #setup buttons
        layout = QVBoxLayout(None, 4)
        addIcon = iconloader.loadIconSet("add", KIcon.Toolbar)
        addButton = KPushButton(addIcon, "", self)
        addButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(addButton)
        removeIcon = iconloader.loadIconSet("remove", KIcon.Toolbar)
        removeButton = KPushButton(removeIcon, "", self)
        removeButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        layout.addWidget(removeButton)
        layout.addItem(QSpacerItem(10, 40))
        mainLayout.addLayout(layout)
        
        #connectionz
        self.connect(self.listView, SIGNAL("executed(QListViewItem *)"), self.executedSlot)
        self.connect(addButton, SIGNAL("clicked()"), self.add)
        self.connect(removeButton, SIGNAL("clicked()"), self.remove)
                
    def addColumns(self):
        for col in self.columns:
            self.listView.addColumn(col)
    
    def executedSlot(self, item ):
        if not item:
            return
        
        values = []
        for i in range(self.listView.columns()):
            values.append(item.text(i))
        dialog = newListViewDialog(self, self.columns, "Edit", values)
        if dialog.exec_loop() == KDialog.Rejected:
            return
        res = dialog.getResults()
        if res == None:
            return
        for i in range(self.listView.columns()):
            item.setText(i, res[i])

    def add(self):
        dialog = newListViewDialog(self, self.columns, "Add", self.columns)
        if dialog.exec_loop() == KDialog.Rejected:
            return
        res = dialog.getResults()
        if res == None:
            return
        lvi = KListViewItem(self.listView, *res)
        lvi.setRenameEnabled(0, True)
    
    def remove(self):
        node = self.listView.selectedItem()
        if not node:
            return
        self.listView.takeItem(node)
        
class newListViewDialog(KDialog):
    def __init__(self, parent, columns, caption, values = None):
        KDialog.__init__(self, parent)
        self.setCaption(caption)
        self.setModal(True)
        self.setFixedWidth(300)
        mainLayout = QVBoxLayout(self, 5, 5)
        self.results = []
        self.columns = columns
        self.lineEdits = []
        
        topLayout = QGridLayout(None, len(columns), 2, 5, 5)
        
        for i, col in enumerate(columns):  
            lab = QLabel(col, self)
            topLayout.addWidget(lab, i, 0)
            line = KLineEdit(self)
            if values != None:
                line.setText(values[i])
            self.lineEdits.append(line)
            topLayout.addWidget(line, i, 1)
                 
        mainLayout.addLayout(topLayout)
        bottomLayout = QHBoxLayout(None, 5)
        bottomLayout.addItem(QSpacerItem(30, 10))
        okButton = KPushButton("OK", self)
        okButton.setDefault(True)
        bottomLayout.addWidget(okButton)
        cancelButton = KPushButton("Cancel", self)
        bottomLayout.addWidget(cancelButton)
        mainLayout.addLayout(bottomLayout)
        
        #connect
        self.connect(okButton, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(cancelButton, SIGNAL("clicked()"), self, SLOT("reject()"))
    
    def getResults(self):
        empties = 0
        for line in self.lineEdits:
            if str(line.text()).strip() == "":
                empties += 1
            self.results.append(str(line.text()))
        if empties == len(self.lineEdits):
            return None
        return self.results
        
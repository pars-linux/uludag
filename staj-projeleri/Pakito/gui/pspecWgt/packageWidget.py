# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

from pisi import specfile as spec
from pisi.dependency import Dependency
from pisi.conflict import Conflict
from pisi.replace import Replace

from packageWidgetUI import PackageWidgetUI
from dialogs.summaryDialog import SummaryDialog
from dialogs.dependencyDialog import DependencyDialog
from dialogs.fileDialog import FileDialog

class packageWidget(QWidget):
    
    class packageTab(PackageWidgetUI):
        def __init__(self, parent):
            PackageWidgetUI.__init__(self, parent)
            il = KGlobal.iconLoader()

            for w in [self.pbLicense, self.pbIsA, self.pbAddRuntimeDep, self.pbAddSummary, self.pbAddReplaces, self.pbAddFile, self.pbAddAdditional, self.pbAddConflict, self.pbAddCOMAR]:
                w.setIconSet(il.loadIconSet("edit_add", KIcon.Toolbar))
            
            for w in [self.pbRemoveRuntimeDep, self.pbRemoveSummary, self.pbRemoveReplaces, self.pbRemoveFile, self.pbRemoveAdditional, self.pbRemoveConflict, self.pbRemoveCOMAR]:
                w.setIconSet(il.loadIconSet("edit_remove", KIcon.Toolbar))

            for w in [self.pbBrowseRuntimeDep, self.pbBrowseSummary, self.pbBrowseReplaces, self.pbBrowseFile, self.pbBrowseAdditional, self.pbBrowseConflict, self.pbBrowseCOMAR]:
                w.setIconSet(il.loadIconSet("fileopen", KIcon.Toolbar))

            self.pbViewCOMAR.setIconSet(il.loadIconSet("filefind", KIcon.Toolbar))
            self.pbViewAdditional.setIconSet(il.loadIconSet("filefind", KIcon.Toolbar))

            self.connect(self.pbAddSummary, SIGNAL("clicked()"), self.slotAddSummary)
            self.connect(self.pbRemoveSummary, SIGNAL("clicked()"), self.slotRemoveSummary)
            self.connect(self.pbBrowseSummary, SIGNAL("clicked()"), self.slotBrowseSummary)
            self.connect(self.lvSummary, SIGNAL("executed(QListViewItem *)"), self.slotBrowseSummary)

            self.connect(self.pbAddRuntimeDep, SIGNAL("clicked()"), self.slotAddRuntimeDep)
            self.connect(self.pbRemoveRuntimeDep, SIGNAL("clicked()"), self.slotRemoveRuntimeDep)
            self.connect(self.pbBrowseRuntimeDep, SIGNAL("clicked()"), self.slotBrowseRuntimeDep)
            self.connect(self.lvRuntimeDep, SIGNAL("executed(QListViewItem *)"), self.slotBrowseRuntimeDep)

            self.connect(self.pbAddReplaces, SIGNAL("clicked()"), self.slotAddReplaces)
            self.connect(self.pbRemoveReplaces, SIGNAL("clicked()"), self.slotRemoveReplaces)
            self.connect(self.pbBrowseReplaces, SIGNAL("clicked()"), self.slotBrowseReplaces)
            self.connect(self.lvReplaces, SIGNAL("executed(QListViewItem *)"), self.slotBrowseReplaces)

            self.connect(self.pbAddConflict, SIGNAL("clicked()"), self.slotAddConflict)
            self.connect(self.pbRemoveConflict, SIGNAL("clicked()"), self.slotRemoveConflict)
            self.connect(self.pbBrowseConflict, SIGNAL("clicked()"), self.slotBrowseConflict)
            self.connect(self.lvConflicts, SIGNAL("executed(QListViewItem *)"), self.slotBrowseConflict)

            self.connect(self.pbAddFile, SIGNAL("clicked()"), self.slotAddFile)
            self.connect(self.pbRemoveFile, SIGNAL("clicked()"), self.slotRemoveFile)
            self.connect(self.pbBrowseFile, SIGNAL("clicked()"), self.slotBrowseFile)
            self.connect(self.lvFiles, SIGNAL("executed(QListViewItem *)"), self.slotBrowseFile)

        def slotBrowseSummary(self):
            lvi = self.lvSummary.selectedItem()
            if not lvi:
                return
            sums = self.getSummaryList()
            dia = SummaryDialog(sums, activeLanguage = str(lvi.text(0)))
            if dia.exec_loop() == QDialog.Rejected:
                return
            self.setSummaryList(dia.getResult())

        def slotRemoveSummary(self):
            lvi = self.lvSummary.selectedItem()
            if lvi:
                self.lvSummary.takeItem(lvi) 

        def slotAddSummary(self):
            sums = self.getSummaryList()
            sums.insert(0, ["","",""])
            dialog = SummaryDialog(sums, parent = self)
            if dialog.exec_loop() == QDialog.Accepted:
                self.setSummaryList(dialog.getResult())

        def setSummaryList(self, l):
            self.lvSummary.clear()
            for sum in l:
                lvi = KListViewItem(self.lvSummary, sum[0], sum[1], sum[2])

        def getSummaryList(self):
            ret = []
            iterator = QListViewItemIterator(self.lvSummary)
            while iterator.current():
                l = []
                lvi = iterator.current()
                l.append(str(lvi.text(0)))
                l.append(unicode(lvi.text(1)))
                l.append(unicode(lvi.text(2)))
                ret.append(l)
                iterator += 1
            return ret

        def slotAddRuntimeDep(self):
            dia = DependencyDialog(parent = self, title = "Runtime Dependencies")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                lvi = KListViewItem(self.lvRuntimeDep, cond, dep)

        def slotRemoveRuntimeDep(self):
            lvi = self.lvRuntimeDep.selectedItem()
            if lvi:
                self.lvRuntimeDep.takeItem(lvi)

        def slotBrowseRuntimeDep(self):
            lvi = self.lvRuntimeDep.selectedItem()
            if not lvi:
                return
            dia = DependencyDialog((str(lvi.text(0)), str(lvi.text(1))), parent = self, title = "Runtime Dependencies")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                lvi.setText(0, cond)
                lvi.setText(1, dep)

        def slotAddReplaces(self):
            dia = DependencyDialog(parent = self, title = "Replaces", secondLabel = "Package:")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                lvi = KListViewItem(self.lvReplaces, cond, dep)

        def slotRemoveReplaces(self):
            lvi = self.lvReplaces.selectedItem()
            if lvi:
                self.lvReplaces.takeItem(lvi)

        def slotBrowseReplaces(self):
            lvi = self.lvReplaces.selectedItem()
            if not lvi:
                return
            dia = DependencyDialog((str(lvi.text(0)), str(lvi.text(1))), parent = self, title = "Replaces", secondLabel = "Package:")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                lvi.setText(0, cond)
                lvi.setText(1, dep)

        def slotAddConflict(self):
            dia = DependencyDialog(parent = self, title = "Conflicts", secondLabel = "Package:")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                lvi = KListViewItem(self.lvConflicts, cond, dep)

        def slotRemoveConflict(self):
            lvi = self.lvConflicts.selectedItem()
            if lvi:
                self.lvConflicts.takeItem(lvi)

        def slotBrowseConflict(self):
            lvi = self.lvConflicts.selectedItem()
            if not lvi:
                return
            dia = DependencyDialog((str(lvi.text(0)), str(lvi.text(1))), parent = self, title = "Conflicts", secondLabel = "Package:")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                lvi.setText(0, cond)
                lvi.setText(1, dep)
        
        def slotAddFile(self):
            dia = FileDialog(parent = self)
            if dia.exec_loop() == QDialog.Accepted:
                res = dia.getResult()
                lvi = KListViewItem(self.lvFiles, res[0], res[1], res[2])

        def slotRemoveFile(self):
            lvi = self.lvFiles.selectedItem()
            if lvi:
                self.lvFiles.takeItem(lvi)

        def slotBrowseFile(self):
            lvi = self.lvFiles.selectedItem()
            if not lvi:
                return
            dia = FileDialog(self, [str(lvi.text(0)), str(lvi.text(1)), str(lvi.text(2))])
            if dia.exec_loop() == QDialog.Accepted:
                res = dia.getResult()
                lvi.setText(0, res[0])
                lvi.setText(1, res[1])
                lvi.setText(2, res[2])

        def fill(self, package):
            # general info
            self.leName.setText(package.name)
            self.leLicense.setText(", ".join(package.license))
            self.leIsA.setText(", ".join(package.isA))
            if package.partOf:
                self.lePartOf.setText(package.partOf)
                
            # summary and descriptions
            self.lvSummary.clear()
            for lang, sum in package.summary.iteritems(): #TODO: summary yok desc varsa?
                lvi = KListViewItem(self.lvSummary, lang, unicode(sum))
                if lang in package.description:
                    lvi.setText(2, unicode(package.description[lang]))
            
            #runtime deps.
            self.lvRuntimeDep.clear()
            runDeps = package.runtimeDependencies()
            for dep in runDeps:
                lvi = KListViewItem(self.lvRuntimeDep, getConstraint(dep), dep.package)
                
            #replaces
            self.lvReplaces.clear()
            for rep in package.replaces:
                lvi = KListViewItem(self.lvReplaces, getConstraint(rep), rep.package)
                
            # files
            self.lvFiles.clear()
            for file in package.files:
                if not file.permanent:
                    file.permanent = ""
                lvi = KListViewItem(self.lvFiles, file.fileType, file.permanent, file.path)                
                
            # additional files
            self.lvAdditionalFiles.clear()
            for file in package.additionalFiles:  
                lvi = KListViewItem(self.lvAdditionalFiles, file.owner, file.permission, file.target, file.filename)  
                
            # conflicts
            self.lvConflicts.clear()
            for conf in package.conflicts:  
                lvi = KListViewItem(self.lvConflicts, getConstraint(conf), conf.package)  
                
            # COMAR 
            self.lvCOMAR.clear()
            for comar in package.providesComar:  #TODO: summary yok desc varsa?
                lvi = KListViewItem(self.lvCOMAR, comar.om, comar.script) 
                 
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
            iterator = QListViewItemIterator(self.lvSummary)
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
            iterator = QListViewItemIterator(self.lvRuntimeDep)
            while iterator.current():
                lvi = iterator.current()
                dep = Dependency()
                getConstraintReverse(str(lvi.text(0)), str(lvi.text(1)), dep)
                package.packageDependencies.insert(0, dep)
                iterator += 1
            
            #get replaces
            package.replaces = []
            iterator = QListViewItemIterator(self.lvReplaces)
            while iterator.current():
                lvi = iterator.current()
                rep = Replace()
                getConstraintReverse(str(lvi.text(0)), str(lvi.text(1)), rep)
                package.replaces.insert(0, rep)
                iterator += 1
            
            #get package files
            package.files = []
            iterator = QListViewItemIterator(self.lvFiles)
            while iterator.current():
                lvi = iterator.current()
                path = spec.Path()
                path.fileType = str(lvi.text(0))
                if str(lvi.text(1)).strip() != "":
                    path.permanent = str(lvi.text(1))
                path.path = str(lvi.text(2))
                package.files.insert(0, path)
                iterator += 1

            #get package additional files
            package.additionalFiles = []
            iterator = QListViewItemIterator(self.lvAdditionalFiles)
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
            iterator = QListViewItemIterator(self.lvConflicts)
            while iterator.current():
                lvi = iterator.current()
                conflict = Conflict()
                getConstraintReverse(str(lvi.text(0)), str(lvi.text(1)), conflict)
                package.conflicts.insert(0,conflict)
                iterator += 1 
        
            #get comar scripts
            package.providesComar = []
            iterator = QListViewItemIterator(self.lvCOMAR)
            while iterator.current():
                lvi = iterator.current()
                comar = spec.ComarProvide()
                if str(lvi.text(0)).strip() != "":
                    comar.om = str(lvi.text(0))
                if str(lvi.text(1)).strip() != "":
                    comar.script = str(lvi.text(1))               
                package.providesComar.insert(0,comar)
                iterator += 1

    def __init__(self, parent, fileLoc = None):
        QWidget.__init__(self, parent)
        pageLayout = QVBoxLayout(self, 6, 11)
        topLayout = QHBoxLayout(pageLayout, 5)
        
        # add/remove package buttons
        pbAddPackage = KPushButton(i18n("Add New Package"), self)
        pbRemovePackage = KPushButton(i18n("Remove Package"), self)
        topSpacer = QSpacerItem(250, 20, QSizePolicy.Expanding)
        topLayout.addWidget(pbAddPackage)
        topLayout.addWidget(pbRemovePackage)
        topLayout.addItem(topSpacer)
        
        self.twPackages = KTabWidget(self)
        pageLayout.addWidget(self.twPackages)
        
        self.connect(pbAddPackage, SIGNAL("clicked()"), self.addPackageSlot)
        self.connect(pbRemovePackage, SIGNAL("clicked()"), self.removePackageSlot)
    
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
            KMessageBox.error(self, i18n("At least one package must exist."), i18n("Error"))
            return
        self.twPackages.removePage(self.twPackages.currentPage())


def cleanTabs(tw):
        for i in range(tw.count()):
            page = tw.currentPage()
            tw.removePage(page)
            page.close()

def getConstraint(dep):
    if dep.version:
        constraint = i18n("Version") + " = " + dep.version
    elif dep.versionTo:
        constraint = i18n("Version") + " <= " + dep.versionTo
    elif dep.versionFrom:
        constraint = i18n("Version") + " >= " + dep.versionFrom
    elif dep.release:
        constraint = i18n("Release") + " = " + dep.release
    elif dep.releaseTo:
        constraint = i18n("Release") + " <= " + dep.releaseTo
    elif dep.releaseFrom:
        constraint = i18n("Release") + " >= " + dep.releaseFrom
    else:
        constraint = ""
    return constraint

def getConstraintReverse(condition, package, dep):
    dep.version = dep.versionFrom = dep.versionTo = None
    dep.release = dep.releaseFrom = dep.releaseTo = None
    
    if condition.startswith(i18n("Version") + " = "):
        dep.version = condition.split("= ")[1]
    elif condition.startswith(i18n("Version") + " <= "):
        dep.versionTo = condition.split("= ")[1]
    elif condition.startswith(i18n("Version") + " >= "):
        dep.versionFrom = condition.split("= ")[1]
    elif condition.startswith(i18n("Release") + " = "):
        dep.release = condition.split("= ")[1]
    elif condition.startswith(i18n("Release") + " <= "):
        dep.releaseTo = condition.split("= ")[1]
    elif condition.startswith(i18n("Release") + " >= "):
        dep.releaseFrom = condition.split("= ")[1]

    dep.package = package

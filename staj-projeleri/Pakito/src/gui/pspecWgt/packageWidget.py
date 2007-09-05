# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

import os
import shutil

from pisi import specfile as spec
from pisi.dependency import Dependency
from pisi.conflict import Conflict
from pisi.replace import Replace

from packageWidgetUI import PackageWidgetUI
from dialogs.summaryDialog import SummaryDialog
from dialogs.dependencyDialog import DependencyDialog
from dialogs.fileDialog import FileDialog
from dialogs.additionalFileDialog import AdditionalFileDialog
from dialogs.comarDialog import COMARDialog

class packageWidget(QWidget):
    
    class packageTab(PackageWidgetUI):
        def __init__(self, parent, filesDir = None, comarDir = None):
            PackageWidgetUI.__init__(self, parent)
            if filesDir:
                self.filesDir = filesDir
            if comarDir:
                self.comarDir = comarDir

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

            self.connect(self.pbAddAdditional, SIGNAL("clicked()"), self.slotAddAdditional)
            self.connect(self.pbViewAdditional, SIGNAL("clicked()"), self.slotViewAdditional)
            self.connect(self.pbRemoveAdditional, SIGNAL("clicked()"), self.slotRemoveAdditional)
            self.connect(self.pbBrowseAdditional, SIGNAL("clicked()"), self.slotBrowseAdditional)
            self.connect(self.lvAdditionalFiles, SIGNAL("executed(QListViewItem *)"), self.slotBrowseAdditional)

            self.connect(self.pbAddCOMAR, SIGNAL("clicked()"), self.slotAddCOMAR)
            self.connect(self.pbViewCOMAR, SIGNAL("clicked()"), self.slotViewCOMAR)
            self.connect(self.pbRemoveCOMAR, SIGNAL("clicked()"), self.slotRemoveCOMAR)
            self.connect(self.pbBrowseCOMAR, SIGNAL("clicked()"), self.slotBrowseCOMAR)
            self.connect(self.lvCOMAR, SIGNAL("executed(QListViewItem *)"), self.slotBrowseCOMAR)

            self.isAPopup = QPopupMenu(self)
            isAList = ["app", "app:console", "app:gui", "app:web", "|", "library", "service", "|", "data", "data:doc", "data:font", "|", "kernel", "driver", "|", "locale"]

            for isa in isAList:
                if isa == "|":
                    self.isAPopup.insertSeparator()
                else:
                    self.isAPopup.insertItem(isa)
            self.connect(self.pbIsA, SIGNAL("clicked()"), self.slotIsAPopup)
            self.connect(self.isAPopup, SIGNAL("activated(int)"), self.slotIsAHandle)

            self.licensePopup = QPopupMenu(self)
            for l in ["GPL", "GPL-2", "GPL-3", "as-is", "LGPL-2", "LGPL-2.1", "BSD", "MIT", "LGPL"]:
                self.licensePopup.insertItem(l)
        
            self.connect(self.pbLicense, SIGNAL("clicked()"), self.slotLicensePopup)
            self.connect(self.licensePopup, SIGNAL("activated(int)"), self.slotLicenseHandle)
            
            self.lvSummary.setSorting(-1)
            self.lvRuntimeDep.setSorting(-1)
            self.lvReplaces.setSorting(-1)
            self.lvFiles.setSorting(-1)
            self.lvAdditionalFiles.setSorting(-1)
            self.lvConflicts.setSorting(-1)
            self.lvCOMAR.setSorting(-1)

        def slotLicensePopup(self):
            self.licensePopup.exec_loop(self.pbLicense.mapToGlobal(QPoint(0,0 + self.pbLicense.height())))

        def slotLicenseHandle(self, id):
            text = str(self.licensePopup.text(id)).replace("&", "")
            curText = str(self.leLicense.text())
            if curText.strip() == "":
                self.leLicense.setText(text)
            else:
                self.leLicense.setText("%s, %s" % (curText, text))

        def slotIsAPopup(self):
            self.isAPopup.exec_loop(self.pbIsA.mapToGlobal(QPoint(0,0 + self.pbIsA.height())))

        def slotIsAHandle(self, id):
            text = str(self.isAPopup.text(id)).replace("&", "")
            curText = str(self.leIsA.text())
            if curText.strip() == "":
                self.leIsA.setText(text)
            else:
                self.leIsA.setText("%s, %s" % (curText, text))

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

        def slotAddAdditional(self):
            dia = AdditionalFileDialog(self)
            if dia.exec_loop() == QDialog.Rejected:
                return
            res = dia.getResult()
            KListViewItem(self.lvAdditionalFiles, res[0], res[1], res[2], res[3])
            if not os.path.isdir(self.filesDir):
                os.mkdir(self.filesDir)
            shutil.copyfile(res[4], self.filesDir + "/" + res[3])

        def slotRemoveAdditional(self):
            lvi = self.lvAdditionalFiles.selectedItem()
            if not lvi:
                return
            file = str(lvi.text(3))
            self.lvAdditionalFiles.takeItem(lvi)
            filePath = self.filesDir + "/" + file
            if os.path.isdir(self.filesDir) and os.path.isfile(filePath):
                os.unlink(filePath)

        def slotBrowseAdditional(self):
            lvi = self.lvAdditionalFiles.selectedItem()
            if not lvi:
                return
            dia = AdditionalFileDialog(self, [str(lvi.text(0)), str(lvi.text(1)), str(lvi.text(2)), str(lvi.text(3))])
            if dia.exec_loop() == QDialog.Rejected:
                return
            res = dia.getResult()
            lvi.setText(0, res[0])
            lvi.setText(1, res[1])
            lvi.setText(2, res[2])
            lvi.setText(3, res[3])
            #TODO: additinal file may be renamed

        def slotViewAdditional(self):
            lvi = self.lvAdditionalFiles.selectedItem()
            if not lvi:
                return
            os.system("kfmclient exec %s" % self.filesDir + "/" + str(lvi.text(3)))

        def slotAddCOMAR(self):
            dia = COMARDialog(self)
            if dia.exec_loop() == QDialog.Rejected:
                return
            res = dia.getResult()
            KListViewItem(self.lvCOMAR, res[0], res[1])
            if not os.path.isdir(self.comarDir):
                os.mkdir(self.comarDir)
            shutil.copyfile(res[2], self.comarDir + "/" + res[1])

        def slotRemoveCOMAR(self):
            lvi = self.lvCOMAR.selectedItem()
            if not lvi:
                return
            file = str(lvi.text(1))
            self.lvCOMAR.takeItem(lvi)
            filePath = self.comarDir + "/" + file
            if os.path.isdir(self.comarDir) and os.path.isfile(filePath):
                os.unlink(filePath)

        def slotBrowseCOMAR(self):
            lvi = self.lvCOMAR.selectedItem()
            if not lvi:
                return
            dia = COMARDialog(self, [str(lvi.text(0)), str(lvi.text(1))])
            if dia.exec_loop() == QDialog.Rejected:
                return
            res = dia.getResult()
            lvi.setText(0, res[0])
            lvi.setText(1, res[1])

        def slotViewCOMAR(self):
            lvi = self.lvCOMAR.selectedItem()
            if not lvi:
                return
            os.system("kfmclient exec %s" % self.comarDir + "/" + str(lvi.text(1)))

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
                 
    def __init__(self, parent, fileLoc = None):
        QWidget.__init__(self, parent)
        pageLayout = QVBoxLayout(self, 6, 11)
        topLayout = QHBoxLayout(pageLayout, 5)
        
        if fileLoc:
            tempDir = os.path.split(fileLoc)[0]
            self.filesDir = tempDir + "/files"
            self.comarDir = tempDir + "/comar"

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
        tab = self.packageTab(self.twPackages, self.filesDir, self.comarDir)
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

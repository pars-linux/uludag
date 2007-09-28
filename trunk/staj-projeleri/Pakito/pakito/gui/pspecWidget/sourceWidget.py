# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

from pisi import specfile as spec
from pisi.dependency import Dependency

import os
import shutil

from pakito.gui.pspecWidget.sourceWidgetUI import SourceWidgetUI
from pakito.gui.pspecWidget.dialogs.summaryDialog import SummaryDialog
from pakito.gui.pspecWidget.dialogs.dependencyDialog import DependencyDialog
from pakito.gui.pspecWidget.dialogs.patchDialog import PatchDialog

class sourceWidget(SourceWidgetUI):
    def __init__(self, parent, fileLoc, xmlUtil):
        SourceWidgetUI.__init__(self, parent)

        self.packageDir = os.path.split(fileLoc)[0]
        self.filesDir = self.packageDir + "/files"
        self.xmlUtil = xmlUtil

        self.lePackager.setPaletteForegroundColor(QColor("black"))
        self.lePackager.setPaletteBackgroundColor(QColor("white"))
        #self.lePackager.setValidator(QRegExpValidator(QRegExp(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.[A-Za-z]{2,4}$"), self))
      
        self.connect(self.pbAddSummary, SIGNAL("clicked()"), self.slotAddSummary)
        self.connect(self.pbRemoveSummary, SIGNAL("clicked()"), self.slotRemoveSummary)
        self.connect(self.pbBrowseSummary, SIGNAL("clicked()"), self.slotBrowseSummary)
        self.connect(self.lvSummary, SIGNAL("executed(QListViewItem *)"), self.slotBrowseSummary)

        self.connect(self.pbAddBuildDep, SIGNAL("clicked()"), self.slotAddBuildDep)
        self.connect(self.pbRemoveBuildDep, SIGNAL("clicked()"), self.slotRemoveBuildDep)
        self.connect(self.pbBrowseBuildDep, SIGNAL("clicked()"), self.slotBrowseBuildDep)
        self.connect(self.lvBuildDep, SIGNAL("executed(QListViewItem *)"), self.slotBrowseBuildDep)
        
        self.connect(self.pbAddPatch, SIGNAL("clicked()"), self.slotAddPatch)
        self.connect(self.pbRemovePatch, SIGNAL("clicked()"), self.slotRemovePatch)
        self.connect(self.pbBrowsePatch, SIGNAL("clicked()"), self.slotBrowsePatch)
        self.connect(self.pbViewPatch, SIGNAL("clicked()"), self.slotViewPatch)
        self.connect(self.lvPatches, SIGNAL("executed(QListViewItem *)"), self.slotBrowsePatch)
        
        il = KGlobal.iconLoader()
        for w in [self.pbLicense, self.pbIsA, self.pbAddSummary, self.pbAddBuildDep, self.pbAddPatch]:
            w.setIconSet(il.loadIconSet("edit_add", KIcon.Toolbar))
        
        for w in [self.pbRemoveSummary, self.pbRemoveBuildDep, self.pbRemovePatch]:
            w.setIconSet(il.loadIconSet("edit_remove", KIcon.Toolbar))
       
        for w in [self.pbBrowseSummary, self.pbBrowseBuildDep, self.pbBrowsePatch]:
            w.setIconSet(il.loadIconSet("fileopen", KIcon.Toolbar))
        
        self.pbViewPatch.setIconSet(il.loadIconSet("filefind", KIcon.Toolbar))

        self.isAPopup = KPopupMenu(self)
        isAList = ["app", "app:console", "app:gui", "app:web", "|", "library", "service", "|", "data", "data:doc", "data:font", "|", "kernel", "driver", "|", "locale"]

        for isa in isAList:
            if isa == "|":
                self.isAPopup.insertSeparator()
            else:
                self.isAPopup.insertItem(isa)
        self.connect(self.pbIsA, SIGNAL("clicked()"), self.slotIsAPopup)
        self.connect(self.isAPopup, SIGNAL("activated(int)"), self.slotIsAHandle)

        self.licensePopup = KPopupMenu(self)
        for l in ["GPL", "GPL-2", "GPL-3", "as-is", "LGPL-2", "LGPL-2.1", "BSD", "MIT", "LGPL"]:
            self.licensePopup.insertItem(l)
        
        self.connect(self.pbLicense, SIGNAL("clicked()"), self.slotLicensePopup)
        self.connect(self.licensePopup, SIGNAL("activated(int)"), self.slotLicenseHandle)

        self.lvSummary.setSorting(-1)
        self.lvBuildDep.setSorting(-1)
        self.lvPatches.setSorting(-1)

        self.connect(self.leName, SIGNAL("textChanged(const QString &)"), self.slotNameChanged)
        self.connect(self.leHomepage, SIGNAL("textChanged(const QString &)"), self.slotHomepageChanged)
        self.connect(self.leLicense, SIGNAL("textChanged(const QString &)"), self.slotLicenseChanged)
        self.connect(self.leIsA, SIGNAL("textChanged(const QString &)"), self.slotIsAChanged)
        self.connect(self.lePartOf, SIGNAL("textChanged(const QString &)"), self.slotPartOfChanged)
        self.connect(self.lePackager, SIGNAL("textChanged(const QString &)"), self.slotPackagerChanged)
        self.connect(self.leEmail, SIGNAL("textChanged(const QString &)"), self.slotEmailChanged)
        self.connect(self.leURI, SIGNAL("textChanged(const QString &)"), self.slotArchiveChanged)
        self.connect(self.leSHA1, SIGNAL("textChanged(const QString &)"), self.slotArchiveChanged)
        self.connect(self.cbType, SIGNAL("activated(const QString &)"), self.slotArchiveChanged)
        
    def slotNameChanged(self, newOne):
        self.xmlUtil.setDataOfTagByPath(str(newOne), "Source", "Name")
        
    def slotHomepageChanged(self, newOne):
        self.xmlUtil.setDataOfTagByPath(str(newOne), "Source", "Homepage")
        
    def slotLicenseChanged(self, newOne):
        while self.xmlUtil.deleteTagByPath("Source", "License"):
            pass
        
        packagerNode = self.xmlUtil.getTagByPath("Source", "Packager")
        licenses = str(newOne).split(", ")
        licenses.reverse()
        for license in licenses:
            self.xmlUtil.addTagBelow(packagerNode, "License", license)
                    
    def slotIsAChanged(self, newOne):
        while self.xmlUtil.deleteTagByPath("Source", "IsA"):
            pass
        
        packagerNode = self.xmlUtil.getTagByPath("Source", "Summary")
        for isa in str(newOne).split(", "):
            self.xmlUtil.addTagAbove(packagerNode, "IsA", isa)
    
    def slotPackagerChanged(self, newOne):
        self.xmlUtil.setDataOfTagByPath(str(newOne), "Source", "Packager", "Name")

    def slotEmailChanged(self, newOne):
        self.xmlUtil.setDataOfTagByPath(str(newOne), "Source", "Packager", "Email")
                    
    def slotPartOfChanged(self, newOne):
        if str(newOne).strip() == "":
            self.xmlUtil.deleteTagByPath("Source", "PartOf")
        else:
            node = self.xmlUtil.getTagByPath("Source", "PartOf")
            if node:
                self.xmlUtil.setDataOfTagByPath(str(newOne), "Source", "PartOf")
            else:
                summaryNode = self.xmlUtil.getTagByPath("Source", "Summary")
                self.xmlUtil.addTagAbove(summaryNode, "PartOf", str(newOne))
        
    def slotArchiveChanged(self, newOne):
        self.xmlUtil.deleteTagByPath("Source", "Archive")
        descNode = self.xmlUtil.getTagByPath("Source", "Description")
        if descNode:
            self.xmlUtil.addTagBelow(descNode, "Archive", str(self.leURI.text()), sha1sum = str(self.leSHA1.text()), type = str(self.cbType.currentText()))
        else:
            sumNode = self.xmlUtil.getTagByPath("Source", "Summary")
            self.xmlUtil.addTagBelow(sumNode, "Archive", str(self.leURI.text()), sha1sum = str(self.leSHA1.text()), type = str(self.cbType.currentText()))

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
    
    def getBuildDepList(self):
        ret = []
        iterator = QListViewItemIterator(self.lvBuildDep)
        while iterator.current():
            l = []
            lvi = iterator.current()
            l.append(str(lvi.text(0)))
            l.append(str(lvi.text(1)))
            ret.append(l)
            iterator += 1
        return ret
    
    def setBuildDepList(self, l):
        self.lvBuildDep.clear()
        for dep in l:
            cond = dep[0].split()
            if len(cond) == 3:
                lvi = KListViewItem(self.lvBuildDep, "%s %s %s" % tuple(cond), dep[1])
            else:
                lvi = KListViewItem(self.lvBuildDep, "", dep[1])

    def slotAddBuildDep(self):
        dia = DependencyDialog(parent = self)
        if dia.exec_loop() == QDialog.Accepted:
            cond, dep = dia.getResult()
            lvi = KListViewItem(self.lvBuildDep, cond, dep)

    def slotRemoveBuildDep(self):
        lvi = self.lvBuildDep.selectedItem()
        if lvi:
           self.lvBuildDep.takeItem(lvi)

    def slotBrowseBuildDep(self):
        lvi = self.lvBuildDep.selectedItem()
        if not lvi:
            return
        dia = DependencyDialog((str(lvi.text(0)), str(lvi.text(1))), parent = self)
        if dia.exec_loop() == QDialog.Accepted:
            cond, dep = dia.getResult()
            lvi.setText(0, cond)
            lvi.setText(1, dep)

    def slotAddPatch(self):
        dia = PatchDialog(self)
        if dia.exec_loop() == QDialog.Accepted:
            res = dia.getResult()
            lvi = KListViewItem(self.lvPatches, res[0], res[1], res[2])
            if not os.path.isdir(self.filesDir):
                os.mkdir(self.filesDir)
            shutil.copyfile(res[3], self.filesDir + "/" + res[2])

    def slotRemovePatch(self):
        lvi = self.lvPatches.selectedItem()
        if not lvi:
            return
        patch = str(lvi.text(2))
        patchPath = self.filesDir + "/" + patch
        if lvi:
            self.lvPatches.takeItem(lvi)
        if os.path.isdir(self.filesDir) and os.path.isfile(patchPath):
            os.unlink(patchPath)

    def slotBrowsePatch(self):
        lvi = self.lvPatches.selectedItem()
        if not lvi:
            return
        if not lvi.text(0) or str(lvi.text(0)).strip() == "":
            level = "0"
        else:
            level = str(lvi.text(0))
        if not lvi.text(1) or str(lvi.text(1)).strip() == "":
            comp = ""
        else:
            comp = str(lvi.text(1))
        dia = PatchDialog(self, [level, comp, str(lvi.text(2))])
        if dia.exec_loop() == QDialog.Accepted:
            res = dia.getResult()
            lvi.setText(0, res[0])
            lvi.setText(1, res[1])
            lvi.setText(2, res[2])
            #TODO: patch file may be renamed

    def slotViewPatch(self):
        lvi = self.lvPatches.selectedItem()
        if not lvi:
            return
        os.system("kfmclient exec %s" % self.filesDir + "/" + str(lvi.text(2)))

    def fill(self, source):
        if source.name:
            self.leName.setText(source.name)
        else:
            self.leName.setText("")
        if source.homepage:
            self.leHomepage.setText(source.homepage)
        else:
            self.leHomepage.setText("")
        self.leLicense.setText(", ".join(source.license))
        self.leIsA.setText(", ".join(source.isA))
        self.lePackager.setText(source.packager.name)
        self.leEmail.setText(source.packager.email)
        if source.partOf:
            self.lePartOf.setText(source.partOf)   
        
        #archive
        self.leURI.setText(source.archive.uri)
        self.cbType.setCurrentText(source.archive.type)
        self.leSHA1.setText(source.archive.sha1sum)

        self.lvSummary.clear()
        for lang, sum in source.summary.iteritems(): #TODO: summary yok desc varsa?
            lvi = KListViewItem(self.lvSummary, lang, unicode(sum))
            if lang in source.description:
                lvi.setText(2, unicode(source.description[lang]))

        self.lvBuildDep.clear()
        for dep in source.buildDependencies:
            lvi = KListViewItem(self.lvBuildDep, getConstraint(dep), dep.package)
        
        self.lvPatches.clear()
        for patch in source.patches:
            if not patch.level:
                patch.level = ""
            if not patch.compressionType:
                patch.compressionType = ""
            lvi = KListViewItem(self.lvPatches, str(patch.level), str(patch.compressionType), patch.filename)
    
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

# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

import os
import shutil

import pisi
from pisi import specfile as spec
from pisi.dependency import Dependency
from pisi.conflict import Conflict
from pisi.replace import Replace

import kdedesigner

from pakito.gui.pspecWidget.packageWidgetUI import PackageWidgetUI
from pakito.gui.pspecWidget.dialogs.summaryDialog import SummaryDialog
from pakito.gui.pspecWidget.dialogs.dependencyDialog import DependencyDialog
from pakito.gui.pspecWidget.dialogs.fileDialog import FileDialog
from pakito.gui.pspecWidget.dialogs.additionalFileDialog import AdditionalFileDialog
from pakito.gui.pspecWidget.dialogs.comarDialog import COMARDialog

class packageWidget(QWidget):

    class packageTab(PackageWidgetUI):
        def __init__(self, parent, filesDir, comarDir, xmlUtil):
            PackageWidgetUI.__init__(self, parent)
            self.filesDir = filesDir
            self.comarDir = comarDir
            self.xmlUtil = xmlUtil
            self.packageDir = os.path.split(filesDir)[0]

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

            self.connect(self.leName, SIGNAL("textChanged(const QString &)"), self.slotNameChanged)
            self.connect(self.leLicense, SIGNAL("textChanged(const QString &)"), self.slotLicenseChanged)
            self.connect(self.leIsA, SIGNAL("textChanged(const QString &)"), self.slotIsAChanged)
            self.connect(self.lePartOf, SIGNAL("textChanged(const QString &)"), self.slotPartOfChanged)


        def slotNameChanged(self, newOne):
            self.xmlUtil.setDataOfTagByPath(str(newOne), "Package", "Name")

        def slotIsAChanged(self, newOne):
            while self.xmlUtil.deleteTagByPath("Package", "IsA"):
                pass

            if str(newOne).strip() == "":
                return

            nameNode = self.xmlUtil.getTagByPath("Package", "Name")
            list = str(newOne).split(", ")
            list.reverse()
            for isa in list:
                self.xmlUtil.addTagBelow(nameNode, "IsA", isa)

        def slotLicenseChanged(self, newOne):
            while self.xmlUtil.deleteTagByPath("Package", "License"):
                pass

            if str(newOne).strip() == "":
                return

            isANode = self.xmlUtil.getTagByPath("Package", "IsA")
            if isANode:
                mainNode = isANode
            else:
                mainNode = self.xmlUtil.getTagByPath("Package", "Name")

            licenses = str(newOne).split(", ")
            licenses.reverse()
            for license in licenses:
                self.xmlUtil.addTagBelow(mainNode, "License", license)

        def slotPartOfChanged(self, newOne):
            if str(newOne).strip() == "":
                self.xmlUtil.deleteTagByPath("Package", "PartOf")
            else:
                node = self.xmlUtil.getTagByPath("Package", "PartOf")
                if node:
                    self.xmlUtil.setDataOfTagByPath(str(newOne), "Package", "PartOf")
                else:
                    runtimeNode = self.xmlUtil.getTagByPath("Package", "RuntimeDependencies")
                    if runtimeNode:
                        self.xmlUtil.addTagAbove(runtimeNode, "PartOf", str(newOne))
                    else:
                        filesNode = self.xmlUtil.getTagByPath("Package", "Files")
                        self.xmlUtil.addTagAbove(filesNode, "PartOf", str(newOne))

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
            self.syncSummary()
            self.syncDescription()

        def slotRemoveSummary(self):
            lvi = self.lvSummary.selectedItem()
            if lvi:
                self.lvSummary.takeItem(lvi)
                self.syncSummary()
                self.syncDescription()

        def slotAddSummary(self):
            sums = self.getSummaryList()
            sums.insert(0, ["","",""])
            dialog = SummaryDialog(sums, parent = self)
            if dialog.exec_loop() == QDialog.Accepted:
                self.setSummaryList(dialog.getResult())
                self.syncSummary()
                self.syncDescription()

        def setSummaryList(self, l):
            self.lvSummary.clear()
            for sum in l:
                KListViewItem(self.lvSummary, sum[0], sum[1], sum[2])

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

        def syncSummary(self):
            #synchronize xml tree with listview
            import pakito.xmlUtil
            summaries = self.getSummaryList()
            while self.xmlUtil.deleteTagByPath("Package", "Summary"):
                pass

            transLoc = self.packageDir + "/translations.xml"
            transXML = None
            if os.path.isfile(transLoc):
                transXML = pakito.xmlUtil.XmlUtil(transLoc)
                while transXML.deleteTagByPath("Package", "Summary"):
                    pass
                transXML.write()

            isaNode = self.xmlUtil.getTagByPath("Package", "Name")
            summaries.reverse()
            for sum in summaries:
                if sum[0] == "en" or sum[0] == "":
                    self.xmlUtil.addTagBelow(isaNode, "Summary", sum[1])
                else:
                    #add to translations.xml
                    if not transXML:
                        import pakito.templates
                        f = open(transLoc, "w")
                        f.write(pakito.templates.translationTemplate % {"source": self.leName.text(), "lang": sum[0], "summary": sum[1]})
                        f.close()
                        transXML = pakito.xmlUtil.XmlUtil(transLoc)
                    else:
                        node = transXML.getTagByPath("Package", "Name")
                        d = {"xml:lang": sum[0]}
                        self.xmlUtil.addTagBelow(node, "Summary", sum[1], **d)
                        transXML.write()
            self.xmlUtil.write()

        def syncDescription(self):
            descs = self.getSummaryList()
            while self.xmlUtil.deleteTagByPath("Package", "Description"):
                pass

            transLoc = self.packageDir + "/translations.xml"
            transXML = None
            if os.path.isfile(transLoc):
                import pakito.xmlUtil
                transXML = pakito.xmlUtil.XmlUtil(transLoc)
                while transXML.deleteTagByPath("Package", "Description"):
                    pass
                transXML.write()

            node = self.xmlUtil.getTagByPath("Package", "Summary")
            descs.reverse()
            for desc in descs:
                if unicode(desc[2]).strip() == "":
                    continue 
                if desc[0] == "en":
                    self.xmlUtil.addTagBelow(node, "Description", desc[2])
                    self.xmlUtil.write()
                else:
                    node2 = transXML.getTagListByPath("Package", "Summary")[-1]
                    d = {"xml:lang": desc[0]}
                    self.xmlUtil.addTagBelow(node2, "Description", desc[2], **d)
                    transXML.write()
            self.xmlUtil.write()

        def slotAddRuntimeDep(self):
            dia = DependencyDialog(parent = self, title = "Runtime Dependencies")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                KListViewItem(self.lvRuntimeDep, cond, dep)
            self.syncRuntimeDep()

        def slotRemoveRuntimeDep(self):
            lvi = self.lvRuntimeDep.selectedItem()
            if lvi:
                self.lvRuntimeDep.takeItem(lvi)
            self.syncRuntimeDep()

        def slotBrowseRuntimeDep(self):
            lvi = self.lvRuntimeDep.selectedItem()
            if not lvi:
                return
            dia = DependencyDialog((str(lvi.text(0)), str(lvi.text(1))), parent = self, title = "Runtime Dependencies")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                lvi.setText(0, cond)
                lvi.setText(1, dep)

            self.syncRuntimeDep()

        def getRuntimeDepList(self):
            ret = []
            iterator = QListViewItemIterator(self.lvRuntimeDep)
            while iterator.current():
                lvi = iterator.current()
                l = [str(lvi.text(0)), str(lvi.text(1))]
                ret.append(l)
                iterator += 1
            return ret

        def setRuntimeDepList(self, l):
            self.lvBuildDep.clear()
            for sum in l:
                KListViewItem(self.lvRuntimeDep, sum[0], sum[1])

        def syncRuntimeDep(self):
            #synchronize xml tree with listview
            import pakito.xmlUtil
            dependency = self.getRuntimeDepList()
            runtimeDepTag=self.xmlUtil.getTagByPath("Package", "RuntimeDependencies")
            node = self.xmlUtil.getTagByPath("Package", "Description")
            if node==False:
                node = self.xmlUtil.getTagByPath("Package", "Summary")
                if node==False:
                    node = self.xmlUtil.getTagByPath("Package", "Name")

            if runtimeDepTag==None:
                self.xmlUtil.addTagBelow(node, "BuildDependencies","")
                self.xmlUtil.write()
            while self.xmlUtil.deleteTagByPath("Package", "RuntimeDependencies", "Dependency"):
                pass

            dependency.reverse()
            dependencyNode = self.xmlUtil.getTagByPath("Package","RuntimeDependencies")
            for dep in dependency:
                if  dep[0] == "":
                    self.xmlUtil.addTag(dependencyNode, "Dependency", dep[1])
                else:
                    node = self.xmlUtil.getTagByPath("Package","RuntimeDependencies")
                    if dep[0].find(">=")!=-1:
                        s=dep[0].partition(">=")
                        key= "%sFrom" % s[0].replace(" ", "")
                        value= s[2].replace(" ", "")
                    elif dep[0].find("<=")!=-1:
                        s=dep[0].partition("<=")
                        key= "%sTo" % s[0].replace(" ", "")
                        value= s[2].replace(" ", "")
                    else:
                        s=dep[0].partition("=")
                        key= s[0].replace(" ", "")
                        value= s[2].replace(" ", "")
                    d = {key:value}
                    self.xmlUtil.addTag(node, "Dependency", dep[1], **d)

            dependency = self.getRuntimeDepList()
            if dependency==[]:
                self.xmlUtil.deleteTagByPath("Package", "RuntimeDependencies")

            self.xmlUtil.write()

        def slotAddReplaces(self):
            dia = DependencyDialog(parent = self, title = "Replaces", secondLabel = "Package:")
            if dia.exec_loop() == QDialog.Accepted:
                cond, dep = dia.getResult()
                KListViewItem(self.lvReplaces, cond, dep)

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
                KListViewItem(self.lvConflicts, cond, dep)

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
                KListViewItem(self.lvFiles, res[0], res[1], res[2])
            self.syncFile()

        def slotRemoveFile(self):
            lvi = self.lvFiles.selectedItem()
            if lvi:
                self.lvFiles.takeItem(lvi)
            self.syncFile()

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

            self.syncFile()

        def getFileList(self):
            ret = []
            iterator = QListViewItemIterator(self.lvFiles)
            while iterator.current():
                lvi = iterator.current()
                l = [str(lvi.text(0)), str(lvi.text(1)), str(lvi.text(2))]
                ret.append(l)
                iterator += 1
            return ret

        def setFileList(self, l):
            self.lvFiles.clear()
            for f in l:
                KListViewItem(self.lvFiles, f[0], f[1],f[2])

        def syncFile(self):
            #synchronize xml tree with listview
            import pakito.xmlUtil
            file = self.getFileList()
            fileTag=self.xmlUtil.getTagByPath("Package", "Files")
            node = self.xmlUtil.getTagByPath("Package")

            if fileTag==None:
                self.xmlUtil.addTag(node, "Files","")
                self.xmlUtil.write()
            while self.xmlUtil.deleteTagByPath("Package", "Files", "Path"):
                pass

            file.reverse()
            fileNode = self.xmlUtil.getTagByPath("Package","Files")
            for f in file:
                if f !=[]:
                    d={}
                    if f[0]!="":
                        d['fileType']=f[0]
                    if f[1]!="":
                        d['permanent']=f[1]
                    fileNode = self.xmlUtil.getTagByPath("Package","Files")
                    self.xmlUtil.addTag(fileNode, "Path",f[2],**d)

            file = self.getFileList()
            if file==[]:
                self.xmlUtil.deleteTagByPath("Package", "Files")

            self.xmlUtil.write()


        def slotAddAdditional(self):
            dia = AdditionalFileDialog(self)
            if dia.exec_loop() == QDialog.Rejected:
                return
            res = dia.getResult()
            KListViewItem(self.lvAdditionalFiles, res[0], res[1], res[2], res[3])
            if not os.path.isdir(self.filesDir):
                os.mkdir(self.filesDir)
            shutil.copyfile(res[4], self.filesDir + "/" + res[3])

            self.syncAdditional()

        def slotRemoveAdditional(self):
            lvi = self.lvAdditionalFiles.selectedItem()
            if not lvi:
                return
            file = str(lvi.text(3))
            self.lvAdditionalFiles.takeItem(lvi)
            filePath = self.filesDir + "/" + file
            if os.path.isdir(self.filesDir) and os.path.isfile(filePath):
                os.unlink(filePath)
            self.syncAdditional()

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

            self.syncAdditional()

        def getAdditionalList(self):
            ret = []
            iterator = QListViewItemIterator(self.lvAdditionalFiles)
            while iterator.current():
                lvi = iterator.current()
                l = [str(lvi.text(0)), str(lvi.text(1)), str(lvi.text(2)), str(lvi.text(2))]
                ret.append(l)
                iterator += 1
            return ret

        def setAdditionalList(self, l):
            self.lvAdditionalFiles.clear()
            for add in l:
                KListViewItem(self.lvAdditionalFiles, add[0], add[1],add[2],add[3])

        def syncAdditional(self):
            #synchronize xml tree with listview
            import pakito.xmlUtil
            additional = self.getAdditionalList()
            additionalTag=self.xmlUtil.getTagByPath("Package", "AdditionalFiles")
            node = self.xmlUtil.getTagByPath("Package")

            if additionalTag==None:
                self.xmlUtil.addTag(node, "AdditionalFiles","")
                self.xmlUtil.write()
            while self.xmlUtil.deleteTagByPath("Package", "AdditionalFiles", "AdditionalFile"):
                pass

            additional.reverse()
            additionalNode = self.xmlUtil.getTagByPath("Package","AdditionalFiles")
            for add in additional:
                if add !=[]:
                    d={}
                    if add[0]!="":
                        d['owner']=add[0]
                    if add[1]!="":
                        d['permission']=add[1]
                    if add[2]!="":
                        d['target']=add[2]
                    additionalNode = self.xmlUtil.getTagByPath("Package","AdditionalFiles")
                    self.xmlUtil.addTag(additionalNode, "AdditionalFile",add[3],**d)

            additional = self.getAdditionalList()
            if additional==[]:
                self.xmlUtil.deleteTagByPath("Package", "AdditionalFiles")

            self.xmlUtil.write()

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
            self.syncCOMAR()

        def slotRemoveCOMAR(self):
            lvi = self.lvCOMAR.selectedItem()
            if not lvi:
                return
            file = str(lvi.text(1))
            self.lvCOMAR.takeItem(lvi)
            filePath = self.comarDir + "/" + file
            if os.path.isdir(self.comarDir) and os.path.isfile(filePath):
                os.unlink(filePath)
            self.syncCOMAR()

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

            self.syncCOMAR()

        def getCOMARList(self):
            ret = []
            iterator = QListViewItemIterator(self.lvCOMAR)
            while iterator.current():
                lvi = iterator.current()
                l = [str(lvi.text(0)), str(lvi.text(1))]
                ret.append(l)
                iterator += 1
            return ret

        def setCOMARList(self, l):
            self.lvCOMAR.clear()
            for c in l:
                KListViewItem(self.lvCOMAR, c[0], c[1])

        def syncCOMAR(self):
            #synchronize xml tree with listview
            import pakito.xmlUtil
            comar = self.getCOMARList()
            comarTag=self.xmlUtil.getTagByPath("Package", "Provides")
            node = self.xmlUtil.getTagByPath("Package")

            if comarTag==None:
                self.xmlUtil.addTag(node, "Provides","")
                self.xmlUtil.write()
            while self.xmlUtil.deleteTagByPath("Package", "Provides", "COMAR"):
                pass

            comar.reverse()
            comarNode = self.xmlUtil.getTagByPath("Package","Provides")
            for c in comar:
                if c !=[]:
                    d={}
                    if c[1]!="":
                        d['script']=c[1]
                    self.xmlUtil.addTag(comarNode, "COMAR",c[0],**d)

            comar = self.getCOMARList()
            if comar==[]:
                self.xmlUtil.deleteTagByPath("Package", "Provides")

            self.xmlUtil.write()


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
            for lang, sum in package.summary.iteritems():
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
            for comar in package.providesComar:
                lvi = KListViewItem(self.lvCOMAR, comar.om, comar.script)

    def __init__(self, parent, fileLoc, xmlUtil):
        QWidget.__init__(self, parent)
        pageLayout = QVBoxLayout(self, 6, 11)
        topLayout = QHBoxLayout(pageLayout, 5)

        tempDir = os.path.split(fileLoc)[0]
        self.filesDir = tempDir + "/files"
        self.comarDir = tempDir + "/comar"
        self.xmlUtil = xmlUtil

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
        tab = self.packageTab(self.twPackages, self.filesDir, self.comarDir, self.xmlUtil)
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

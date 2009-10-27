#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt4 import QtGui, QtCore, uic
import gettext

_ = gettext.gettext

from screens import ScrRepo
from screens import ScrMedia
from screens import ScrSystemType
from screens import ScrUsers
from screens import ScrGrub
from screens import ScrPackages

screenId = {"":""}

class Pardusman(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("screens/mainWindowUi.ui", self)

        self.getWidgets()
        self.initialize()
        self.setMainWindow()
        
        self.projectData = {"user":{},  "grub":{}}

    def getWidgets(self):
        self.avail_screens = [ScrRepo.Widget(),
                              ScrMedia.Widget(),
                              ScrSystemType.Widget(),
                              ScrUsers.Widget(),
                              ScrGrub.Widget()]

    def initialize(self):
        leftPanel = ""
        for screen in self.avail_screens:
            _w = screen
            self.pageStack.addWidget(_w)
            sId = self.pageStack.indexOf(_w)
            sCaption = _w.windowTitle()
            screenId[sId] = sCaption

            if sId == 2:
                leftPanel += self.putBold(sCaption)
            else:
                leftPanel += self.putBr(sCaption)

        self.pixSteps.setText(leftPanel)
        self.pageStack.setCurrentIndex(2)

    def setWidgets(self):
        for widget in self.avail_screens:
            self.pageStack.addWidget(widget)

    def getCurrent(self):
        return self.pageStack.indexOf(self.pageStack.currentWidget())

    def stackMove(self,where):
        if where<=2:
            where = 2
        if where>len(self.avail_screens):
            where = len(self.avail_screens)+1

        self.pageStack.setCurrentIndex(where)
        _w = self.pageStack.currentWidget()
        self.pageDesc.setText(_(_w.desc))

        _w.show()

        # hide next and show finish buttons on last screen
        if self.getCurrent() == len(screenId):
            self.buttonNext.hide()
            self.buttonFinish.show()
        else:
            self.buttonNext.show()
            self.buttonFinish.hide()

        # hide back button on first screen
        if self.getCurrent()-1 == 1:
            self.buttonBack.hide()
        else:
            self.buttonBack.show()

    def slotNext(self):
        where= self.getCurrent()
        
        if self.checkScreen(where):
            self.collectData(where)
            
            # skip user screen for install cd
            if not self.avail_screens[2].radioLive.isChecked() and self.getCurrent() == 4:
                next = where + 2
            else:
                next = where + 1
    
            stepBatch = ""
    
            for sId in screenId:
                if  sId <= len(screenId):
                    if sId == next:
                        stepBatch+= self.putBold(screenId[sId])
                    else:
                        stepBatch+= self.putBr(screenId[sId])
    
            self.pixSteps.setText(stepBatch)
            self.stackMove(next)

    def putBr(self, item):
        return unicode("» ") + item + "<br>"

    def putBold(self, item):
        return "<b>" + unicode("» ") + item + "</b><br>"

    def slotBack(self):
        where = self.getCurrent()
        
        if self.checkScreen(where):
            self.collectData(where)
            
            if not self.avail_screens[2].radioLive.isChecked() and self.getCurrent() == 6:
                prev =  where - 2
            else:
                prev = where - 1
     
            stepBatch = ""
            for sId in screenId:
                if  sId < len(screenId) and not sId == 1:
                    if sId == prev:
                        stepBatch+= self.putBold(screenId[sId])
                    else:
                        stepBatch+= self.putBr(screenId[sId])
            stepBatch+= self.putBr(screenId[len(screenId)])
            self.pixSteps.setText(stepBatch)
    
            self.stackMove(prev)

    def checkScreen(self,  where):
        def error(widget,  message):
            widget.labelError.setText(message)
            widget.frameError.setVisible(1)
        def success(widget):
            widget.frameError.setVisible(0)
        
        widget =  self.avail_screens[where-2]

        if where == 2: # repo screen
            if not widget.radioPardus.isChecked() and not widget.radioOther.isChecked():
                error(widget, "Please choose a repo")
                return 0
            else:
                success(widget)
                return 1

        elif where == 3: # media screen
            if (widget.radioCD.isChecked() or widget.radioSL.isChecked() or widget.radioDL.isChecked() or widget.radioExternal.isChecked()):
                if widget.radioExternal.isChecked():
                    if widget.sliderSize.value() == 0:
                        error(widget,  "Please specify disk size")
                        return 0
                success(widget)
                return 1
            else:
                error(widget,  "Please choose a media")
                return 0
                
        elif where == 5: #users screen
            if not widget.pass1.text() or not widget.username.text() or not widget.admin_pass1.text():
                error(widget,  "Please fill all fields")
                return 0
            if widget.hasError == 0:
                return 1
            else:
                return 0
        else:
            return 1

    def collectData(self,  where):
        widget =  self.avail_screens[where-2]

        if where == 2: # Repo screen
            if widget.radioPardus.isChecked():
                self.projectData["repo"] = ["http://paketler.pardus.org.tr/pardus-2008/pisi-index.xml.bz2"]
 #               not implemented yet. pardusman support only one repo.
 #               if widget.checkContrib.isChecked():
 #                   self.projectData["repo2"] = "http://paketler.pardus.org.tr/contrib-2008/pisi-index.xml.bz2"
            else:
                self.projectData["repo"] = [widget.lineOther.text()]

        elif where == 3: # Media screen
            options = {"CD":"CD",
                       "DVD SL (4 GB)":"SL",
                       "DVD DL (8 GB)":"DL",
                       "External Disk":"ED-%s" % widget.sliderSize.value()}

            try:
                self.projectData["media"] = options[widget.chosen]
            except AttributeError:
                self.projectData["media"] = ""

        elif where == 4: # Type screen
            options = {"Install CD":"install", "Live CD":"live"}

            try:
                self.projectData["type"] = options[widget.chosen]
            except AttributeError:
                self.projectData["type"] = ""

        elif where == 5: # Users screen
            # projectData{"user":{"LoginName":["Real Name", "Password", isAdmin}}
            self.projectData["user"][str(widget.username.text())] = [str(widget.realname.text()), str(widget.pass1.text()),  widget.admin.isChecked()]
            self.projectData["user"]["root"] = [str(widget.admin_pass1.text())]

        elif where == 6: # Grub screen
            self.projectData["grub"]["image"] = widget.chosen
            self.projectData["grub"]["options"]  = []
            
            if widget.checkContinue.isChecked():
                self.projectData["grub"]["options"].append("continue")
            if widget.checkMemory.isChecked():
                self.projectData["grub"]["options"].append("memory")

    def slotFinish(self):
#        self.collectData(self.getCurrent())
#        
#        filename = QtGui.QFileDialog.getSaveFileName(self,  _("Save Project File"),  ("/home"))
#        
#        self.createProjectFile(filename)
#        
        self.showPackages()
    
    def showPackages(self):        
        self.packagesWidget = ScrPackages.Widget()
        
        self.packagesWidget.repo_uri = self.projectData["repo"][0]
        self.packagesWidget.systemType = self.projectData["type"]
        self.packagesWidget.takeList()
        self.packagesWidget.fillComponents()
        
        self.packagesWidget.show()
    
    def setMainWindow(self):
        self.pageDesc.setText(_("Welcome to Pardus CD/DVD/USB Distribution Wizard"))
        
        icon = QtGui.QPixmap(QtCore.QString("data/pardusman.png"))
        self.pageIcon.setPixmap(icon)
        
        self.buttonCancel.setText(_("&Cancel"))
        self.buttonBack.setText(_("&Back"))
        self.buttonNext.setText(_("&Next"))
        self.buttonFinish.setText(_("Finish"))

        self.buttonFinish.hide()
        self.buttonBack.hide()

        self.connect(self.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        self.connect(self.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        self.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("quit()"))
        self.connect(self.buttonFinish, QtCore.SIGNAL("clicked()"), self.slotFinish)

        self.setWidgets()
    
    def createProjectFile(self,  filename):
        import piksemel
        
        doc = piksemel.newDocument("PardusmanProject")
        doc.setAttribute("type", self.projectData["type"])
        doc.setAttribute("media", self.projectData["media"])
#        doc.insertTag("Title").insertData(values["Project Name"])
        if self.projectData["type"] == "live":
            users = doc.insertTag("Users")
            for username in self.projectData["user"].iterkeys():
                user = users.insertTag("User")
                if username == "root":
                    user.setAttribute("username",  username)
                    user.setAttribute("passwd",  self.projectData["user"]["root"][0])
                else:
                    user.setAttribute("username",  username)
                    user.setAttribute("name",  self.projectData["user"][username][0])
                    user.setAttribute("passwd",  self.projectData["user"][username][1])
                    user.setAttribute("isAdmin",  str(self.projectData["user"][username][2]))
            grub = doc.insertTag("grub")
            grub.insertTag("image").insertData(self.projectData["grub"]["image"])
            for option in self.projectData["grub"]["options"]:
                grub.insertTag("option").insertData(option)
        doc.insertTag("WorkDir").insertData("/tmp/pw_tmp")

        paks = doc.insertTag("PackageSelection")
        paks.setAttribute("repo_uri", "|".join(self.projectData["repo"]))
        #values["Components"].sort()
        #for item in values["Components"]:
        #   paks.insertTag("SelectedComponent").insertData(item)
        #values["Packages"].sort()
        #for item in values["Packages"]:
        #    paks.insertTag("SelectedPackage").insertData(item)
    
        data = doc.toPrettyString()
        f = file(filename, "w")
        f.write(data)
        f.close()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    pm = Pardusman()
    pm.show()
    sys.exit(app.exec_())


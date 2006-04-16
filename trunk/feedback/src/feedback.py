#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  Bahadır Kandemir <bahadir@pardus.org.tr>

from ConfigParser import ConfigParser
import os
import sys
import time
import urllib

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# Wizard Pages
from welcomedlg import WelcomeDlg
from experiencedlg import ExperienceDlg
from purposedlg import PurposeDlg
from usagedlg import UsageDlg
from questiondlg import QuestionDlg
from opiniondlg import OpinionDlg
from personalinfodlg import PersonalInfoDlg
from hardwareinfodlg import HardwareInfoDlg
from upload import UploadDlg
from goodbyedlg import GoodbyeDlg

def AboutData():
    description = "Pardus Feedback Tool"
    version = "1.0.2"

    about_data = KAboutData("feedback", "Pardus Feedback Tool", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005, 2006 UEKAE/TÜBİTAK", None, None, "bahadir@pardus.org.tr")

    about_data.addAuthor("Bahadır Kandemir", None, "bahadir@pardus.org.tr")
    about_data.addCredit("S. Çağlar Onur", "Previous Maintainer", None)
    about_data.addCredit("Görkem Çetin",  "Interface Design", None)
    return about_data

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

def loadIconSet(name, group=KIcon.Desktop):
        return KGlobal.iconLoader().loadIconSet(name, group)

class Form(KWizard):
    def __init__(self, parent = None, name = None, modal = 0):
        KWizard.__init__(self, parent, name, modal)

        self.resize(QSize(600,373).expandedTo(self.minimumSizeHint()))
        self.setCaption(i18n("Feedback Wizard"))

        self.setIcon(loadIcon("feedback"))
          
        # Images
        self.image_feedback = QPixmap(locate("data", "feedback/feedback_right.png"))

        self.pageWelcomeDlg = WelcomeDlg()
        self.addPage(self.pageWelcomeDlg, i18n("Welcome"))

        self.pageExperienceDlg = ExperienceDlg()
        self.addPage(self.pageExperienceDlg, i18n("Experience"))

        self.pagePurposeDlg = PurposeDlg()
        self.addPage(self.pagePurposeDlg, i18n("Purpose"))

        self.pageUsageDlg = UsageDlg()
        self.addPage(self.pageUsageDlg, i18n("Usage"))

        self.pageQuestionDlg = QuestionDlg()
        self.addPage(self.pageQuestionDlg, i18n("Questions"))

        self.pageOpinionDlg = OpinionDlg()
        self.addPage(self.pageOpinionDlg, i18n("Opinions"))

        self.pagePersonalInfoDlg = PersonalInfoDlg()
        self.addPage(self.pagePersonalInfoDlg, i18n("Personal Info"))

        self.pageHardwareInfoDlg = HardwareInfoDlg()
        self.addPage(self.pageHardwareInfoDlg, i18n("Hardware Info"))

        self.pageUploadDlg = UploadDlg()
        self.addPage(self.pageUploadDlg, i18n("Uploading"))

        self.pageGoodbyeDlg  = GoodbyeDlg()
        self.addPage(self.pageGoodbyeDlg, i18n("Goodbye!"))

        # Pixmaps
        self.pageExperienceDlg.experiencePixmap.setPixmap(self.image_feedback)
        self.pageGoodbyeDlg.goodbyePixmap.setPixmap(self.image_feedback)
        self.pageHardwareInfoDlg.hardwareInfoPixmap.setPixmap(self.image_feedback)
        self.pageOpinionDlg.opinionPixmap.setPixmap(self.image_feedback)
        self.pageHardwareInfoDlg.hardwareInfoPixmap.setPixmap(self.image_feedback)
        self.pagePurposeDlg.purposePixmap.setPixmap(self.image_feedback)
        self.pageQuestionDlg.questionPixmap.setPixmap(self.image_feedback)
        self.pageUploadDlg.hardwareInfoPixmap.setPixmap(self.image_feedback)
        self.pageUsageDlg.usagePixmap.setPixmap(self.image_feedback)
        self.pageWelcomeDlg.welcomePixmap.setPixmap(self.image_feedback)
        self.pagePersonalInfoDlg.hardwareInfoPixmap.setPixmap(self.image_feedback)

        # Buttons
        n = self.nextButton()
        QObject.connect(n, SIGNAL("clicked()"), self.next_clicked)
        #
        b = self.backButton()
        QObject.connect(b, SIGNAL("clicked()"), self.back_clicked)
        #
        f = self.finishButton()
        QObject.connect(f, SIGNAL("clicked()"), self.finish_clicked)

        # Common elements & options
        for i in range(self.pageCount()):
            # No help button
            self.setHelpEnabled(self.page(i), 0)
        
        self.pageUploadDlg.buttonRetry.hide()
        QObject.connect(self.pageUploadDlg.buttonRetry, SIGNAL("clicked()"), self.button_retry_clicked)
        
        # Buttons on last 2 pages
        self.setBackEnabled(self.pageUploadDlg, 0)
        self.setNextEnabled(self.pageUploadDlg, 0)
        self.setBackEnabled(self.pageGoodbyeDlg, 0)
        self.setFinishEnabled(self.pageGoodbyeDlg, 1)

        # Create upload thread
        self.thread_1 = thread_upload()

    def __tr(self,s,c = None):
        return qApp.translate("Feedback",s,c)

    def next_clicked(self):
        if self.currentPage() == self.pageUploadDlg:
            self.thread_1.start()
        
    def back_clicked(self):
        pass

    def finish_clicked(self):
        pass

    def button_retry_clicked(self):
        self.pageUploadDlg.buttonRetry.hide()
        self.pageUploadDlg.labelStatus.setText("")
        self.thread_1.start()
        

class thread_upload(QThread):
    def run(self):
        upload = {}
        text = ""
        # Collect hardware information
        upload['hardware'] = ""
        if not w.pageHardwareInfoDlg.hardwareInfoBox.isChecked():
            text += i18n("Collecting hardware information...")
            w.pageUploadDlg.labelStatus.setText(text)
            stdin, stdout, stderr = os.popen3("uhinv -f text")
            if "".join(stderr):
                text += i18n("<font color=\"#ff0000\">Failed</font><br>\n")
                text += i18n("<font color=\"#ff0000\">Be sure that Feedback is fully installed.</font><br>\n")
                w.pageUploadDlg.labelStatus.setText(text)
                w.pageUploadDlg.buttonRetry.show()
                return
            else:
                text += i18n("<font color=\"#008800\">Done</font><br>\n")
                upload['hardware'] = "".join(stdout)
                w.pageUploadDlg.labelStatus.setText(text)
        # Upload data to dev. center
        text += i18n("Uploading data...")
        w.pageUploadDlg.labelStatus.setText(text)
        # Experience
        upload['exp'] = 0
        if w.pageExperienceDlg.questionOne.isChecked():
            upload['exp'] = 1
        elif w.pageExperienceDlg.questionTwo.isChecked():
            upload['exp'] = 2
        elif w.pageExperienceDlg.questionThree.isChecked():
            upload['exp'] = 3
        elif w.pageExperienceDlg.questionFour.isChecked():
            upload['exp'] = 4
        # Purpose
        upload['purpose'] = 0
        if w.pagePurposeDlg.checkBoxDaily.isChecked():
            upload['purpose'] += 1
        if w.pagePurposeDlg.checkBoxHobby.isChecked():
            upload['purpose'] += 2
        if w.pagePurposeDlg.checkBoxInt.isChecked():
            upload['purpose'] += 4
        if w.pagePurposeDlg.checkBoxBus.isChecked():
            upload['purpose'] += 8
        if w.pagePurposeDlg.checkBoxEnt.isChecked():
            upload['purpose'] += 16
        if w.pagePurposeDlg.checkBoxEdu.isChecked():
            upload['purpose'] += 32
        # Usage
        upload['usage'] = 0
        if w.pageUsageDlg.usagecheckBoxOne.isChecked():
            upload['usage'] += 1
        if w.pageUsageDlg.usagecheckBoxTwo.isChecked():
            upload['usage'] += 2
        if w.pageUsageDlg.usagecheckBoxThree.isChecked():
            upload['usage'] += 4
        # Question
        upload['question'] = 0
        if w.pageQuestionDlg.questionOne.isChecked():
            upload['question'] = 1
        elif w.pageQuestionDlg.questionTwo.isChecked():
            upload['question'] = 2
        elif w.pageQuestionDlg.questionThree.isChecked():
            upload['question'] = 3
        # Opinion
        upload['opinion'] = str(w.pageOpinionDlg.opinionEdit.text())
        # Personal
        upload['email'] = str(w.pagePersonalInfoDlg.lineEmail.text())
        upload['email_announce'] = w.pagePersonalInfoDlg.CheckBoxAnnounce.isChecked()

        # Upload!
        try:
            params = urllib.urlencode(upload)
            f = urllib.urlopen(url_upload, params)
            s = f.read()
            if s != '1':
                raise IOError, "ConnectionError"
        except:
            text += i18n("<font color=\"#ff0000\">Failed</font><br>\n")
            text += i18n("<font color=\"#ff0000\">Be sure that you're connected to the Internet.</font><br>\n")
            w.pageUploadDlg.labelStatus.setText(text)
            w.pageUploadDlg.buttonRetry.show()
            return
        else:
            text += i18n("<font color=\"#008800\">Done</font><br>\n")
            w.pageUploadDlg.labelStatus.setText(text)

        #
        w.setNextEnabled(w.pageUploadDlg, 1)

def main():
    global w, url_upload

    conf = ConfigParser()
    try:
        conf.read("/etc/feedback.conf")
        url_upload = conf.get("general", "url")
    except:
        url_upload = "http://www.pardus.org.tr/feedback/feedback.py"

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)

    if not KUniqueApplication.start():
        print i18n("Feedback tool is already running!")
        return

    kapp = KUniqueApplication(True, True, True)
    w = Form()
    kapp.setMainWidget(w)
    sys.exit(w.exec_loop())

if __name__ == "__main__":
    main()

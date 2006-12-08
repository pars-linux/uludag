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

# JSON
from simplejson import dumps as json_encode

# Version
version = "1.0.5"

def AboutData():
    global version
    description = "Pardus Feedback Tool"

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
    def __init__(self, parent = None, name = None):
        KWizard.__init__(self, parent, name)

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

    def __tr(self,s,c = None):
        return qApp.translate("Feedback",s,c)

    def next_clicked(self):
        if self.currentPage() == self.pageUploadDlg:
            thread_up.start()

    def button_retry_clicked(self):
        self.pageUploadDlg.buttonRetry.hide()
        self.pageUploadDlg.labelStatus.setText("")
        self.thread_up.start()
        

class thread_upload(QThread):
    def run(self):
        upload = {"version": version}
        text = ""

        # Collect hardware information
        if not w.pageHardwareInfoDlg.hardwareInfoBox.isChecked():

            def readProcFile(file, label):
                for i in open(file).readlines():
                    if i.startswith(label):
                        return i.split(":")[1].strip()

            text += i18n("Collecting hardware information...")
            w.pageUploadDlg.labelStatus.setText(text)

            upload["hw"] = {}
            upload["hw"]["memtotal"] = readProcFile("/proc/meminfo", "MemTotal").split()[0]
            upload["hw"]["swaptotal"] = readProcFile("/proc/meminfo", "SwapTotal").split()[0]
            upload["hw"]["cpu_model"] = readProcFile("/proc/cpuinfo", "model name")
            upload["hw"]["cpu_speed"] = readProcFile("/proc/cpuinfo", "cpu MHz")
            upload["hw"]["kernel"] = open("/proc/version").read().split()[2]

            text += i18n("<font color=\"#008800\">Done</font><br>\n")
            w.pageUploadDlg.labelStatus.setText(text)

        # Upload data to dev. center
        text += i18n("Uploading data...")
        w.pageUploadDlg.labelStatus.setText(text)

        # Experience
        upload['experience'] = 0
        if w.pageExperienceDlg.questionOne.isChecked():
            upload['experience'] = 1
        elif w.pageExperienceDlg.questionTwo.isChecked():
            upload['experience'] = 2
        elif w.pageExperienceDlg.questionThree.isChecked():
            upload['experience'] = 3
        elif w.pageExperienceDlg.questionFour.isChecked():
            upload['experience'] = 4

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
        upload['use_where'] = 0
        if w.pageUsageDlg.usagecheckBoxOne.isChecked():
            upload['use_where'] += 1
        if w.pageUsageDlg.usagecheckBoxTwo.isChecked():
            upload['use_where'] += 2
        if w.pageUsageDlg.usagecheckBoxThree.isChecked():
            upload['use_where'] += 4

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

        # Encode dictionary
        upload = json_encode(upload)

        # Upload!
        try:
            params = urllib.urlencode({"data": upload})
            f = urllib.urlopen(url_upload, params)
            s = f.read()
        except:
            text += i18n("<font color=\"#ff0000\">Failed</font><br>\n")
            text += i18n("<font color=\"#ff0000\">Unable to connect feedback database.</font><br>\n")
            w.pageUploadDlg.labelStatus.setText(text)
            w.pageUploadDlg.buttonRetry.show()
            return

        if s == "0":
            text += i18n("<font color=\"#008800\">Done</font><br>\n")
            w.pageUploadDlg.labelStatus.setText(text)
            w.setNextEnabled(w.pageUploadDlg, 1)
        else:
            text += i18n("<font color=\"#ff0000\">Failed</font><br>\n")

            if s == "1":
                text += i18n("<font color=\"#ff0000\">Feedback seems to be broken. Data is corrupted.</font><br>\n")
            elif s == "2":
                text += i18n("<font color=\"#ff0000\">Server does not support this version. Please update feedback tool.</font><br>\n")
            elif s == "3":
                text += i18n("<font color=\"#ff0000\">Feedback seems to be broken. Data is missing.</font><br>\n")
            elif s == "4":
                text += i18n("<font color=\"#ff0000\">Feedback database is offline.</font><br>\n")
            elif s == "5":
                text += i18n("<font color=\"#ff0000\">You've already sent feedback.</font><br>\n")
            else:
                text += i18n("<font color=\"#ff0000\">Feedback database has errors.</font><br>\n")

            w.pageUploadDlg.labelStatus.setText(text)
            w.pageUploadDlg.buttonRetry.show()

def quit():
    thread_up.exit()

def main():
    global w, url_upload, thread_up

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

    # Kill thread on exit
    QObject.connect(kapp, SIGNAL("aboutToQuit()"), quit)

    # Attach main widget
    w = Form()
    kapp.setMainWidget(w)

    # Upload thread
    thread_up = thread_upload()

    sys.exit(w.exec_loop())

if __name__ == "__main__":
    main()

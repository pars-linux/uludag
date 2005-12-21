#!/usr/bin/python
# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
import os
import sys
import time

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

# Gettext
import gettext
t = gettext.translation("feedback", fallback=True)
_ = t.ugettext

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

def AboutData():
    description = "Pardus Feedback Tool"
    version = "1.0_rc1"

    about_data = KAboutData("feedback", "Pardus Feedback Tool", version, \
                            description, KAboutData.License_GPL,
                            "(C) 2005 UEKAE/TÜBİTAK", None, None, "bahadir@haftalik.net")

    about_data.addAuthor(I18N_NOOP("Bahadır Kandemir"), None, "bahadir@haftalik.net")
    about_data.addCredit(I18N_NOOP("S. Çağlar Onur"), "Previous Maintainer", None)
    about_data.addCredit(I18N_NOOP("Görkem Çetin"),  "Interface Design", None)
    return about_data

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

def loadIconSet(name, group=KIcon.Desktop):
        return KGlobal.iconLoader().loadIconSet(name, group)

class Form(KWizard):
    def __init__(self, parent = None, name = None, modal = 0, fl = 0):
        KWizard.__init__(self, parent, name, modal, fl)

        self.resize(QSize(600,373).expandedTo(self.minimumSizeHint()))
        
        # Images
        self.image_feedback = QPixmap("feedback.png")

        self.pageWelcomeDlg = WelcomeDlg()
        self.addPage(self.pageWelcomeDlg, self.__tr("Welcome"))

        self.pageExperienceDlg = ExperienceDlg()
        self.addPage(self.pageExperienceDlg, self.__tr("Experience"))

        self.pagePurposeDlg = PurposeDlg()
        self.addPage(self.pagePurposeDlg, self.__tr("Purpose"))

        self.pageUsageDlg = UsageDlg()
        self.addPage(self.pageUsageDlg, self.__tr("Usage"))

        self.pageQuestionDlg = QuestionDlg()
        self.addPage(self.pageQuestionDlg, self.__tr("Questions"))

        self.pageOpinionDlg = OpinionDlg()
        self.addPage(self.pageOpinionDlg, self.__tr("Opinions"))

        self.pagePersonalInfoDlg = PersonalInfoDlg()
        self.addPage(self.pagePersonalInfoDlg, self.__tr("Personal Info"))

        self.pageHardwareInfoDlg = HardwareInfoDlg()
        self.addPage(self.pageHardwareInfoDlg, self.__tr("Hardware Info"))

        self.pageUploadDlg = UploadDlg()
        self.addPage(self.pageUploadDlg, self.__tr("Uploading"))

        self.pageGoodbyeDlg  = GoodbyeDlg()
        self.addPage(self.pageGoodbyeDlg, self.__tr("Goodbye!"))

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
        text = ""
        done = _("<font color=\"#008800\">Done</font><br>\n")
        failed = _("<font color=\"#ff0000\">Failed</font><br>\n")
        # Collect hardware information
        if not w.pageHardwareInfoDlg.hardwareInfoBox.isChecked():
            text += _("Collecting hardware information...")
            w.pageUploadDlg.labelStatus.setText(text)
            stdin, stdout, stderr = os.popen3("uhinv -f text")
            if "".join(stderr):
                text += failed
                w.pageUploadDlg.labelStatus.setText(text)
                w.pageUploadDlg.buttonRetry.show()
                return
            else:
                text += done
                w.pageUploadDlg.labelStatus.setText(text)
        # Upload data to dev. center
        text += _("Uploading data...")
        w.pageUploadDlg.labelStatus.setText(text)
        try:
            # FIXME
            pass
        except:
            text += failed
            w.pageUploadDlg.labelStatus.setText(text)
            w.pageUploadDlg.buttonRetry.show()
            return
        else:
            text += done
            w.pageUploadDlg.labelStatus.setText(text)
        #
        w.setNextEnabled(w.pageUploadDlg, 1)

def main():
    global w, url

    conf = ConfigParser()
    try:
        conf.read("/etc/feedback.conf")
        url = conf.get("general", "url")
    except:
        url = "http://www.uludag.org.tr/feedback.py"

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)

    if not KUniqueApplication.start():
        print _("Feedback tool is already running!")
        return

    kapp = KUniqueApplication(True, True, True)
    w = Form()
    kapp.setMainWidget(w)
    sys.exit(w.exec_loop())

if __name__ == "__main__":
    main()

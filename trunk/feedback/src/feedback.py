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

from feedbackdlg import FeedbackForm

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

class Form(FeedbackForm):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        FeedbackForm.__init__(self, parent, name, modal, fl)

        # Images
        self.image_feedback = QPixmap("feedback.png")

        # Pixmaps
        self.welcomePixmap.setPixmap(self.image_feedback)
        self.experiencePixmap.setPixmap(self.image_feedback)
        self.purposePixmap.setPixmap(self.image_feedback)
        self.usagePixmap.setPixmap(self.image_feedback)
        self.questionPixmap.setPixmap(self.image_feedback)
        self.opinionPixmap.setPixmap(self.image_feedback)
        self.hardwareInfoPixmap.setPixmap(self.image_feedback)
        self.uploadPixmap.setPixmap(self.image_feedback)
        self.goodbyePixmap.setPixmap(self.image_feedback)

        # Buttons
        n = self.nextButton()
        n.setIconSet(loadIconSet("forward", KIcon.Small))
        n.setText(_("Next"))
        QObject.connect(n, SIGNAL("clicked()"), self.next_clicked)
        #
        b = self.backButton()
        b.setIconSet(loadIconSet("back", KIcon.Small))
        b.setText(_("Back"))
        QObject.connect(b, SIGNAL("clicked()"), self.back_clicked)
        #
        c = self.cancelButton()
        c.setIconSet(loadIconSet("cancel", KIcon.Small))
        c.setText(_("Cancel"))
        #
        f = self.finishButton()
        f.setIconSet(loadIconSet("ok", KIcon.Small))
        f.setText(_("Finish"))
        QObject.connect(f, SIGNAL("clicked()"), self.finish_clicked)

        # Common elements & options
        for i in range(self.pageCount()):
            # No help button
            self.setHelpEnabled(self.page(i), 0)
        
        self.buttonRetry.hide()
        QObject.connect(self.buttonRetry, SIGNAL("clicked()"), self.button_retry_clicked)
        
        # Buttons on pages M and N
        self.setBackEnabled(self.PageUpload, 0)
        self.setNextEnabled(self.PageUpload, 0)
        self.setBackEnabled(self.PageThank, 0)
        self.setFinishEnabled(self.PageThank, 1)

        # Create upload thread
        self.thread_1 = thread_upload()

    def next_clicked(self):
        if self.currentPage() == self.PageUpload:
            self.thread_1.start()
        
    def back_clicked(self):
        pass

    def finish_clicked(self):
        pass

    def button_retry_clicked(self):
        self.buttonRetry.hide()
        self.labelStatus.setText("")
        self.thread_1.start()
        

class thread_upload(QThread):
    def run(self):
        text = ""
        done = _("<font color=\"#008800\">Done</font><br>\n")
        failed = _("<font color=\"#ff0000\">Failed</font><br>\n")
        # Collect hardware information
        if not w.hardwareInfoBox.isChecked():
            text += _("Collecting hardware information...")
            w.labelStatus.setText(text)
            stdin, stdout, stderr = os.popen3("uhinv -f text")
            if "".join(stderr):
                text += failed
                w.labelStatus.setText(text)
                w.buttonRetry.show()
                return
            else:
                text += done
                w.labelStatus.setText(text)
        # Upload data to dev. center
        text += _("Uploading data...")
        w.labelStatus.setText(text)
        try:
            # FIXME
            pass
        except:
            text += failed
            w.labelStatus.setText(text)
            w.buttonRetry.show()
            return
        else:
            text += done
            w.labelStatus.setText(text)
        #
        w.setNextEnabled(w.PageUpload, 1)

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

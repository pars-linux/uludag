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

class FeedbackForm(QWizard):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QWizard.__init__(self, parent, name, modal, fl)

        # Form settings
        self.setName("FeedbackForm")
        self.setCaption(_("Pardus Feedback Tool"))
        self.setMinimumSize(QSize(600, 350))
        self.setMaximumSize(QSize(600, 350))
        self.resize(QSize(600, 350))

        # Images
        self.image_feedback = QPixmap("feedback.png")

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

        # Page 0 - Welcome
        self.page_0 = QWidget(self, "page_0")
        #
        self.label_0 = QLabel(self.page_0, "label_0")
        self.label_0.setGeometry(QRect(150, 80, 400, 200))
        self.label_0.setAlignment(QLabel.AlignTop)
        text = _("With this small wizard, you can send your messages to Pardus\n" \
               "developers and help Pardus be the best Linux in the world.\n" \
               "\n" \
               "The information you will give here will accelerate Pardus development.\n" \
               "Please click on \"Forward\" button for the next step.")
        self.label_0.setText(text)
        #
        self.addPage(self.page_0, QString(_("<b>Welcome</b>")))

        # Page 1 - Your experience level
        self.page_1 = QWidget(self, "page_1")
        #
        self.box_0 = QButtonGroup(self.page_1, "box_0")
        self.box_0.setGeometry(QRect(150, 80, 400, 140))
        self.box_0.setFrameShape(QButtonGroup.NoFrame)
        #
        self.radio_exp1 = QRadioButton(self.box_0, "radio_exp1")
        self.radio_exp1.setGeometry(QRect(20, 10, 360, 19))
        self.radio_exp1.setText(QString(_("New user")))
        self.radio_exp1.setChecked(1)
        self.box_0.insert(self.radio_exp1)
        #
        self.radio_exp2 = QRadioButton(self.box_0, "radio_exp2")
        self.radio_exp2.setGeometry(QRect(20, 40, 360, 19))
        self.radio_exp2.setText(QString(_("Home/office productivity user")))
        self.box_0.insert(self.radio_exp2)
        #
        self.radio_exp3 = QRadioButton(self.box_0, "radio_exp3")
        self.radio_exp3.setGeometry(QRect(20, 70, 360, 19))
        self.radio_exp3.setText(QString(_("Experienced user")))
        self.box_0.insert(self.radio_exp3)
        #
        self.radio_exp4 = QRadioButton(self.box_0, "radio_exp4")
        self.radio_exp4.setGeometry(QRect(20, 100, 360, 19))
        self.radio_exp4.setText(QString(_("Experienced system administrator")))
        self.box_0.insert(self.radio_exp4)
        #
        self.addPage(self.page_1, QString(_("<b>Your experience level</b>")))
        
        # Page 2 - Why do you use Pardus?
        self.page_2 = QWidget(self, "page_2")
        #
        self.label_multi = QLabel(self.page_2, "label_multi")
        self.label_multi.setGeometry(QRect(150, 80, 400, 19))
        self.label_multi.setText(_("(You can click on multiple items.)"))
        #
        self.box_1 = QButtonGroup(self.page_2, "box_1")
        self.box_1.setGeometry(QRect(150, 110, 400, 140))
        self.box_1.setFrameShape(QButtonGroup.NoFrame)
        #
        self.check_why1 = QCheckBox(self.box_1, "check_why1")
        self.check_why1.setGeometry(QRect(20, 10, 180, 19))
        self.check_why1.setText(QString(_("Daily use")))
        #
        self.check_why2 = QCheckBox(self.box_1, "check_why2")
        self.check_why2.setGeometry(QRect(20, 40, 180, 19))
        self.check_why2.setText(QString(_("It's my hobby")))
        #
        self.check_why3 = QCheckBox(self.box_1, "check_why3")
        self.check_why3.setGeometry(QRect(20, 70, 180, 19))
        self.check_why3.setText(QString(_("For internet access")))
        #
        self.check_why4 = QCheckBox(self.box_1, "check_why4")
        self.check_why4.setGeometry(QRect(190, 10, 180, 19))
        self.check_why4.setText(QString(_("For business")))
        #
        self.check_why5 = QCheckBox(self.box_1, "check_why5")
        self.check_why5.setGeometry(QRect(190, 40, 180, 19))
        self.check_why5.setText(QString(_("Entertainment purposes")))
        #
        self.check_why6 = QCheckBox(self.box_1, "check_why6")
        self.check_why6.setGeometry(QRect(190, 70, 180, 19))
        self.check_why6.setText(QString(_("Educational purposes")))
        #
        self.addPage(self.page_2, QString(_("<b>Why do you use Pardus?</b>")))

        # Page 3 - Where do you use Pardus?
        self.page_3 = QWidget(self, "page_3")
        #
        self.label_multi2 = QLabel(self.page_3, "label_multi2")
        self.label_multi2.setGeometry(QRect(150, 80, 400, 19))
        self.label_multi2.setText(_("(You can click on multiple items.)"))
        #
        self.box_2 = QButtonGroup(self.page_3, "box_2")
        self.box_2.setGeometry(QRect(150, 110, 400, 140))
        self.box_2.setFrameShape(QButtonGroup.NoFrame)
        #
        self.check_where1 = QCheckBox(self.box_2, "check_where1")
        self.check_where1.setGeometry(QRect(20, 10, 150, 19))
        self.check_where1.setText(QString(_("At home")))
        #
        self.check_where2 = QCheckBox(self.box_2, "check_where2")
        self.check_where2.setGeometry(QRect(20, 40, 150, 19))
        self.check_where2.setText(QString(_("At work")))
        #
        self.check_where3 = QCheckBox(self.box_2, "check_where3")
        self.check_where3.setGeometry(QRect(20, 70, 150, 19))
        self.check_where3.setText(QString(_("At school")))
        #
        self.addPage(self.page_3, QString(_("<b>Where do you use Pardus?</b>")))
        
        # Page 4 - How does Pardus fit your needs?
        self.page_4 = QWidget(self, "page_4")
        #
        self.box_2 = QButtonGroup(self.page_4, "box_2")
        self.box_2.setGeometry(QRect(150, 80, 400, 140))
        self.box_2.setFrameShape(QButtonGroup.NoFrame)
        #
        self.radio_fit1 = QRadioButton(self.box_2, "radio_fit1")
        self.radio_fit1.setGeometry(QRect(20, 10, 360, 19))
        self.radio_fit1.setText(QString(_("Very satisfying. Pardus fulfils my requirements.")))
        self.radio_fit1.setChecked(1)
        self.box_2.insert(self.radio_fit1)
        #
        self.radio_fit2 = QRadioButton(self.box_2, "radio_fit2")
        self.radio_fit2.setGeometry(QRect(20, 40, 360, 19))
        self.radio_fit2.setText(QString(_("Good, however it lacks some capabilities.")))
        self.box_2.insert(self.radio_fit2)
        #
        self.radio_fit3 = QRadioButton(self.box_2, "radio_fit3")
        self.radio_fit3.setGeometry(QRect(20, 70, 360, 19))
        self.radio_fit3.setText(QString(_("It has insufficient areas.")))
        self.box_2.insert(self.radio_fit3)
        #
        self.addPage(self.page_4, QString(_("<b>How does Pardus fit your needs?</b>")))
        
        # Page 5 - Your opinions about Pardus
        self.page_5 = QWidget(self, "page_5")
        #
        self.label_tip = QLabel(self.page_5, "label_tip")
        self.label_tip.setGeometry(QRect(150, 80, 400, 40))
        text = _("(Ease of installation and use, capability of software,\n" \
                 "general quality, adaptability, suitability to requirements, etc.)")
        self.label_tip.setText(text)
        #
        self.text_opinion = QTextEdit(self.page_5, "text_opinion")
        self.text_opinion.setGeometry(QRect(150, 130, 400, 120))
        #
        self.addPage(self.page_5, QString(_("<b>Your opinions about Pardus?</b>")))
        
        # Page 6 - Computer information
        self.page_6 = QWidget(self, "page_6")
        #
        self.label_warn = QLabel(self.page_6, "label_warn")
        self.label_warn.setGeometry(QRect(150, 80, 440, 120))
        self.label_warn.setTextFormat(QLabel.RichText)
        text = _("Pardus Hardware CollectInfo Wizard will now gather information from<br>\n" \
                 "your hardware, including CPU, memory and network cards. This<br>\n" \
                 "information will be sent to Pardus Development Center, in order to<br>\n" \
                 "build more stable and secure Pardus. You will need an internet<br>\n" \
                 "access for this operation to complete.<br>\n" \
                 "<br>\n" \
                 "<b>Note that we will not collect any of your personal documents.</b>")
        self.label_warn.setText(text)
        #
        self.check_hw = QCheckBox(self.page_6, "check_hw")
        self.check_hw.setGeometry(QRect(150, 220, 420, 19))
        self.check_hw.setText(QString(_("Don't send hardware information.")))
        #
        self.addPage(self.page_6, QString(_("<b>Computer information</b>")))

        # Page M - Upload data
        self.page_M = QWidget(self, "page_M")
        #
        self.label_status = QLabel(self.page_M, "label_status")
        self.label_status.setGeometry(QRect(150, 80, 400, 150))
        self.label_status.setTextFormat(QLabel.RichText)
        self.label_status.setAlignment(QLabel.AlignTop)
        #
        self.button_retry = QPushButton(self.page_M, "button_retry")
        self.button_retry.setGeometry(QRect(150, 200, 150, 21))
        self.button_retry.setText(QString(_("Retry")))
        self.button_retry.hide()
        QObject.connect(self.button_retry, SIGNAL("clicked()"), self.button_retry_clicked)
        #
        self.addPage(self.page_M, QString(_("<b>Uploading collected data</b>")))

        # Page N - Finish
        self.page_N = QWidget(self, "page_N")
        #
        self.label_bye = QLabel(self.page_N, "label_bye")
        self.label_bye.setGeometry(QRect(150, 80, 440, 120))
        self.label_bye.setTextFormat(QLabel.RichText)
        self.label_bye.setAlignment(QLabel.AlignTop)
        text = _("We have collected all necessary information and sent \n" \
                 "to Pardus developers.\n" \
                 "<p>\n" \
                 "Thank you for your support to Pardus operating system.")
        self.label_bye.setText(text)
        #
        self.addPage(self.page_N, QString(_("<b>Thank you</b>")))

        # Common elements & options
        for i in range(self.pageCount()):
            # No help button
            self.setHelpEnabled(self.page(i), 0)
            # Pixmap
            p = QLabel(self.page(i), "pixmap_feedback_%d" % i)
            p.setGeometry(QRect(0, 0, 137, 274))
            p.setPixmap(self.image_feedback)
            p.setScaledContents(1)
            # Step
            if i not in [0, self.pageCount() - 1, self.pageCount() - 2]:
                l = QLabel(self.page(i), "label_step_%d" % i)
                l.setGeometry(QRect(150, 10, 400, 21))
                l.setPaletteForegroundColor(QColor(77, 77, 77))
                l.setFrameShape(QLabel.NoFrame)
                l.setFrameShadow(QLabel.Plain)
                l.setText(_("<b>Step %d of %d</b>") % (i, self.pageCount() - 3))
            # Title
            t = QLabel(self.page(i), "label_title_%d" % i)
            t.setGeometry(QRect(150, 40, 400, 40))
            t.setPaletteForegroundColor(QColor(0, 0, 0))
            t.setFrameShape(QLabel.NoFrame)
            t.setFrameShadow(QLabel.Plain)
            t.setText("<h2>%s</h2>" % unicode(self.title(self.page(i))))
        
        # Buttons on pages M and N
        self.setNextEnabled(self.page_M, 0)
        self.setBackEnabled(self.page_M, 0)
        self.setBackEnabled(self.page_N, 0)
        self.setFinishEnabled(self.page_N, 1)

        # Create upload thread
        self.thread_1 = thread_upload()

    def next_clicked(self):
        new = self.currentPage()
        old = self.page(self.indexOf(new) - 1)
        if self.indexOf(new) == self.pageCount() - 2:
            self.thread_1.start()
        
    def back_clicked(self):
        pass

    def finish_clicked(self):
        pass

    def button_retry_clicked(self):
        self.button_retry.hide()
        self.label_status.setText("")
        self.thread_1.start()
        

class thread_upload(QThread):
    def run(self):
        text = ""
        done = _("<font color=\"#008800\">Done</font><br>\n")
        failed = _("<font color=\"#ff0000\">Failed</font><br>\n")
        # Collect hardware information
        if not w.check_hw.isChecked():
            text += _("Collection hardware information...")
            w.label_status.setText(text)
            stdin, stdout, stderr = os.popen3("uhinv -f text")
            if "".join(stderr):
                text += failed
                w.label_status.setText(text)
                w.button_retry.show()
                return
            else:
                text += done
                w.label_status.setText(text)
        # Upload data to dev. center
        text += _("Uploading data...")
        w.label_status.setText(text)
        try:
            # FIXME
            pass
        except:
            text += failed
            w.label_status.setText(text)
            w.button_retry.show()
            return
        else:
            text += done
            w.label_status.setText(text)
        #
        w.setNextEnabled(w.page_M, 1)

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
    w = FeedbackForm()
    kapp.setMainWidget(w)
    sys.exit(w.exec_loop())

if __name__ == "__main__":
    main()

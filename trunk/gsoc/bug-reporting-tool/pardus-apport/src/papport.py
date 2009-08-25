#!/usr/bin/python
# -*- coding: utf-8 -*-

import apport.ui
import sys
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from threading import Thread

import gui, subprocess, os, dbus

from gui.bugtoolMain import Ui_bugtoolUI
from gui import (errorScreen, reportScreen, messageScreen, choicesScreen,
                 userpassScreen, progressScreen)


class PApport(QtGui.QWidget, apport.ui.UserInterface):

    def __init__(self, app, parent=None):
        apport.ui.UserInterface.__init__(self)
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_bugtoolUI()

        self.ui.setupUi(self)
        self.active_widgets = []
        self.screenData = None
        self.moveInc = 1
        self.app = app
        self.app.setQuitOnLastWindowClosed(True)
        self.running = True
        self.is_active = False

        self.waitNextClick = QtCore.QWaitCondition()
        self.mutex = QtCore.QMutex()

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"),
                               self.slotNext)
        QtCore.QObject.connect(self.ui.buttonCancel,
                               QtCore.SIGNAL("clicked()"),
                               self.closeEvent)

        # Forcing show() on __init__() since run_argv() may block the UI
        self.show()
        rect  = QtGui.QDesktopWidget().screenGeometry()
        self.move(rect.width()/2 - self.width()/2, rect.height()/2 -\
                  self.height()/2)
        self.app.exec_()
        self.run_argv()


    def slotNext(self):
        if not self.is_active:
            sys.exit(0)
        if hasattr(self.current, 'execute') and self.current.execute():
            self.is_active = False
            self.waitNextClick.wakeAll()

    def closeEvent(self, event=None):
        sys.exit(0)

    def _updateMenu(self):
        self.menuText = ""
        current = self.ui.mainStack.currentIndex() - 1
        for index, each in enumerate(self.active_widgets):
            title = each.windowTitle()
            if index  == current:
                self.menuText += self.putBold(title)
            else:
                self.menuText += self.putBr(title)
        self.ui.labelMenu.setText(self.menuText)

    def getCur(self, d):
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    def setCurrent(self, wid=None):
        if wid:
            self.stackMove(wid)

    def appendScreen(self, screen):
        widget = screen.Widget()
        self.is_active = True
        self.active_widgets.append(widget)
        self.ui.mainStack.addWidget(widget)
        self.ui.mainStack.setCurrentWidget(widget)
        self._updateMenu()

    def set_current_title(self, title):
        self.current.setWindowTitle(title)
        self._updateMenu()

    def putBr(self, item):
        return unicode(u"» ") + item + "<br>"

    def putBold(self, item):
        return "<b>" + unicode(u"» ") + item + "</b><br>"

    def wait_for_next_click(self):
        self.mutex.lock()
        self.waitNextClick.wait(self.mutex)

    def wait_user_input(self):
        t = Thread(target=self.wait_for_next_click)
        t.start()
        while t.is_alive():
            self.app.processEvents()

    @property
    def current(self):
        return self.ui.mainStack.currentWidget()

    # Apport interface
    def ui_present_crash(self, desktop_entry):
        self.appendScreen(errorScreen)

        if desktop_entry:
            name = desktop_entry.getName()
            heading = 'Sorry, %s closed unexpectedly' % name
        elif self.report.has_key('ExecutablePath'):
            name = os.path.basename(self.report['ExecutablePath'])
            heading = 'Sorry, the program "%s" closed unexpectedly.' % name
        else:
            name = self.cur_package
            heading = 'Sorry, %s closed unexpectedly.' % name

        self.set_current_title(name)
        self.current.ui.heading.setText(heading)
        self.current.ui.text.setText('If you were not doing anything '
                                     'confidential (entering passwords or '
                                     'other private information), you can help'
                                     'to improve the application by reporting'
                                     'the problem.')
        self.current.setCheckBox('&Ignore future crashes of this program'
                                 ' version')
        self.wait_user_input()

        blacklist = self.current.ui.checkBox.isChecked()
        return {'action': 'report', 'blacklist': blacklist}

    def ui_present_kernel_error(self):
        self.appendScreen(errorScreen)

        message = 'Your system encountered a serious kernel problem.'
        annotate = ''
        if self.report.has_key('Annotation'):
            annotate = self.report['Annotation'] + '\n\n'
        annotate += ('You can help the developers to fix the problem by '
                     'reporting it.')

        self.set_current_title('Kernel problem')
        self.current.ui.heading.setText(message)
        self.current.ui.text.setText(annotate)

        self.wait_user_input()
        return 'report'

    def ui_persent_package_error(self):
        self.appendScreen(errorScreen)

        name = self.report['Package']
        heading = 'Sorry, the package "%s" failed to install or upgrade.' % name
        text = ('You can help the developers to fix the package by reporting'\
                ' the problem')

        self.wait_user_input()
        return 'report'

    def ui_present_report_details(self):
        self.appendScreen(reportScreen)

        name = self.report.get('Package')
        if name is not None:
            name = name.split()[0]
        else:
            name = 'Generic Error'
        heading = 'Send problem report to the developers?'
        text = ('You may check below the data that will be sent to the '
                'developers as well as choose whether you want to send a '
                'complete report or a reduced one.')

        self.set_current_title(name)
        self.current.ui.heading.setText(heading)
        self.current.ui.text.setText(text)

        # complete/reduce radio buttons
        if self.report.has_key('CoreDump') and \
                self.report.has_useful_stacktrace():
            complete_size = self.format_filesize(self.get_complete_size())
            reduced_size = self.format_filesize(self.get_reduced_size())
            self.current.ui.setText('Complete report (recommended; %s)' %
                                    complete_size)
            self.current.ui.setText('Reduced report (slow Internet connection;'
                                    ' %s)' % reduced_size)
        else:
            self.current.ui.options.hide()

        # Filling report details
        details = self.current.ui.details
        for key in self.report:
            item = QtGui.QTreeWidgetItem([key])
            details.addTopLevelItem(item)

            if not hasattr(self.report[key], 'gzipvalue') and \
               hasattr(self.report[key], 'isspace') and \
               not self.report._is_binary(self.report[key]):
                lines = self.report[key].splitlines()
                for line in lines:
                    QtGui.QTreeWidgetItem(item, [line])
                if len(lines) < 4:
                    item.setExpanded(True)
            else:
                QtGui.QTreeWidgetItem(item, ['(binary data)'])
        details.header().hide()

        self.wait_user_input()

        if self.current.ui.reduced.isChecked():
            return 'reduced'
        else:
            return 'full'

    def ui_info_message(self, title, text):
        self.appendScreen(messageScreen)
        self.set_current_title('Information')
        self.current.ui.heading.setText(title)
        self.current.ui.text.setText(text)
        self.wait_user_input()

    def ui_error_message(self, title, text):
        self.appendScreen(messageScreen)
        self.set_current_title('Error!')
        self.current.ui.heading.setText(title)
        self.current.ui.text.setText(text)
        self.wait_user_input()

    def ui_question_yesno(self, text):
        # TODO: check if this would be better when stacked in the wizard
        response = kdeui.KMessageBox.questionYesNoCancel(None, text,
                                      QtCore.QString(),
                                      kdeui.KStandardGuiItem.yes(),
                                      kdeui.KStandardGuiItem.no(),
                                      kdeui.KStandardGuiItem.cancel())
        if response == kdeui.KMessageBox.Yes:
            return True
        if response == kdeui.KMessageBox.No:
            return False
        return None

    def ui_question_file(self, text):
        # TODO: check if this would be better when stacked in the wizard
        response = QtGui.QFileDialog.getOpenFileName(None, text)
        if response.length() == 0:
            return None
        return str(response)

    def ui_question_choice(self, text, options, multiple):
        ''' Show a question with predefined choices.

        @options is a list of strings to present.
        @multiple - if True, choices should be QCheckBoxes, if False then
        should be QRadioButtons.

        Return list of selected option indexes, or None if the user cancelled.
        If multiple is False, the list will always have one element.
        '''
        self.appendScreen(choicesScreen)

        self.set_current_title('Apport Choices')
        self.current.ui.text.setText(text)

        for option in options:
            self.current.add_choice(option, multiple)

        self.wait_user_input()
        return self.current.get_response()

    def ui_question_userpass(self, text):
        '''Show a Username/Password dialog.

        Return a tuple (user, pass) or None if cancelled.
        '''
        self.appendScreen(userpassScreen)

        self.set_current_title('Credentials')
        self.current.ui.text.setText(text)

        self.wait_user_input()
        return self.current.get_userpass()

    def ui_start_info_collection_progress(self):
        self.appendScreen(progressScreen)

        self.set_current_title('Collecting data')
        self.current.ui.heading.setText('Collecting Problem Information')
        self.current.ui.text.setText('The collected information can be sent '
                                     'to the developers to improve the '
                                     'application. This might take a few '
                                     'minutes.')
        self.current.set_progress()
        self.ui.buttonNext.setEnabled(False)

    def ui_pulse_info_collection_progress(self):
        self.current.set_progress()

    def ui_stop_info_collection_progress(self):
        self.ui.buttonNext.setEnabled(True)

    def ui_start_upload_progress(self):
        self.appendScreen(progressScreen)

        self.set_current_title('Uploading Report')
        self.current.ui.heading.setText('Uploading Problem Information')
        self.current.ui.text.setText('The collected information is being sent'
                                     ' to the bug tracking system. This might'
                                     ' take a few minutes.')
        self.ui.buttonNext.setEnabled(False)

    def ui_set_upload_progress(self, progress):
        self.current.set_progress(progress)

    def ui_stop_upload_progress(self):
        self.ui.buttonNext.setEnabled(True)


if __name__ == "__main__":
    # About data
    appName     = "papport"
    catalog     = ""
    programName = ki18n("papport")
    version     = "0.1"
    description = ki18n("Pardus' Apport KDE GUI")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009 Pardus")
    text        = ki18n("none")
    homePage    = "www.pardus.org.tr"
    bugEmail    = "pinar@pardus.org.tr"

    aboutData   = KAboutData(appName,catalog, programName, version, description,
                                license, copyright,text, homePage, bugEmail)

    KCmdLineArgs.init([''], aboutData)
    app =  kdeui.KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    papport = PApport(app)
    #app.exec_()


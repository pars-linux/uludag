#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QLocale
from PyQt4.QtCore import QTranslator

from puding.resources import ResourceManager


class RunApplicationInterface:
    def __init__(self):
        self.res = ResourceManager()

        try:
            self.run()

        except ImportError:
            self.first_run()


    def run(self):
        from puding.ui.qt.main_window import MainWindow


        app = QApplication(sys.argv)
        locale = QLocale.system().name()
        translator = QTranslator()
        translator.load("%s/translations/puding_%s.qm" % (self.res.DEV_HOME, locale))
        app.installTranslator(translator)
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

    #TODO: This function should work in another OS's too.
    def first_run(self):
        import glob
        import os


        ui_files = glob.glob("%s/ui/qt/ui/*.ui" % self.res.DEV_HOME)
        rc_files = glob.glob("%s/ui/qt/*.qrc" % self.res.DEV_HOME)

        for qt_file in ui_files + rc_files:
            if qt_file.endswith(".qrc"):
                command = "pyrcc4"
                file_name_ext = "rc"

            else:
                command = "pyuic4"
                file_name_ext = "ui"

            qt_file_name = os.path.split(qt_file)[-1]
            py_file_name = os.path.splitext(qt_file_name)[0] + "_%s.py" % file_name_ext

            print("converting %s as %s..." % (qt_file_name, py_file_name))
            os.system("/usr/bin/%s %s -o %s/ui/qt/%s" % \
                (command, qt_file, self.res.DEV_HOME, py_file_name))

        #And then..
        self.run()


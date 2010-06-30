#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Taha Doğan Güneş <tdgunes@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from PyQt4.QtCore import (QFile, QTextStream, SIGNAL, 
                           QTranslator,  QLocale, QIODevice,
                           QFileInfo)
from PyQt4.QtGui import ( QApplication, QFileDialog,
                         QMessageBox, QMainWindow)
import sys
from main_ui import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    """Class for (MainWindow + Ui_MainWindow)"""
    def __init__(self):
        """SIGNALS and setupUi"""
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connect(self.actionOpen, SIGNAL("triggered()"), self.load_file)
        self.path = ""
    def load_file(self):
        """Loading a text file to the self.textEdit"""
        fileobject = None
        self.path = QFileDialog.getOpenFileName(self, "TextEditor","")
        try:
            fileobject = QFile(self.path)
            if not fileobject.open(QIODevice.ReadOnly):
                raise IOError, unicode(fileobject.errorString())
            textstream = QTextStream(fileobject)
            textstream.setCodec("UTF-8")
            self.textEdit.setPlainText(textstream.readAll())
            self.setWindowTitle("%s - TextEditor" % 
                                QFileInfo(self.path).fileName())
        except(IOError, OSError), error:
            QMessageBox.warning(self, 
                               self.tr("TextEditor - Load Error",
                                       "Unable to load %s:%s" % 
                                       (self.filename, error)))
        finally:
            if fileobject is not None:
                fileobject.close()
    def save_file(self):
        """Saving file to the path where getting from QFileDialog"""
        fileobject = None
        self.path = QFileDialog.getSaveFileName(self,
                                                "TextEditor", 
                                                self.tr("unnamed"))
        try:
            fileobject = QFile(self.path)
            if not fileobject.open(QIODevice.WriteOnly):
                raise IOError, unicode(fileobject.errorString())
            textstream = QTextStream(fileobject)
            textstream.setCodec("UTF-8")
            textstream << self.textEdit.toPlainText()
        except (IOError, OSError), error:
            QMessageBox.warning(self, 
                                self.tr("TextEditor - Save Error"), 
                                self.tr("Unable to save %s: %s" % 
                                self.path, error))
        finally:
            if fileobject is not None:
                fileobject.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    locale = QLocale.system().name()
    translator = QTranslator()
    translator.load("texteditor_%s.qm" % locale)
    app.installTranslator(translator)
    main_window = MainWindow()
    main_window.show()
    app.exec_()


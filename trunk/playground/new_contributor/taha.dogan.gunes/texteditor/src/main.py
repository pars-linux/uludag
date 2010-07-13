#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Main.py - TextEditor's main file
"""
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
    """
    Class for (MainWindow + Ui_MainWindow)
    """
    def __init__(self):
        """
        SIGNALS and setupUi
        """
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connect(self.actionExit,
                     SIGNAL("triggered()"), self.close)
        self.connect(self.actionOpen, 
                     SIGNAL("triggered()"), self.load_file)
        self.connect(self.actionSave, 
                     SIGNAL("triggered()"), self.save_file)
        self.connect(self.actionSave_As, 
                     SIGNAL("triggered()"), self.save_as_file)
        self.connect(self.actionNew, 
                     SIGNAL("triggered()"), self.new_file)
        self.connect(self.textEdit.document(), 
                     SIGNAL("modificationChanged(bool)"), self.modified)
        
        
        self.path = ""
        
        
    def closeEvent(self, event):
        """
        When user tries to quit the application.
        """
        if self.ready_to_go() is False:
            event.ignore()
            
            
    def ready_to_go(self):
        """
        To check unsaved changes and asking to the user.
        """
        if self.textEdit.document().isModified():
            question = QMessageBox.question(self,
                                            self.tr("TextEditor - Unsaved Changes"),
                                            self.tr("Do you want to save changes ?"),
                                            QMessageBox.Yes|QMessageBox.No|
                                            QMessageBox.Cancel)
            if question == QMessageBox.Cancel:
                return False
            elif question == QMessageBox.Yes:
                self.save_file()
                return True
            else:
                return True
        
        
    def load_file(self):
        """
        Loading a text file to the self.textEdit
        """
        self.ready_to_go()
        fileobject = None
        self.path = QFileDialog.getOpenFileName(self, "TextEditor","")
        try:
            fileobject = QFile(self.path)
            if not fileobject.open(QIODevice.ReadOnly):
                raise IOError, unicode(fileobject.errorString())
            textstream = QTextStream(fileobject)
            textstream.setCodec("UTF-8")
            self.textEdit.setPlainText(textstream.readAll())
            self.textEdit.document().setModified(False)
            print self.textEdit.document().isModified()
            self.setWindowTitle("%s - TextEditor" % 
                                QFileInfo(self.path).fileName())
        except(IOError, OSError), error:
            QMessageBox.warning(self, 
                                self.tr("TextEditor - Load Error"),
                                self.tr("Unable to load {0} : {1}".format(self.path,
                                                                        error)))
            self.path = ""
        finally:
            if fileobject is not None:
                fileobject.close()
                
                
    def save_as_file(self):
        """
        Saving file with a new name or a new extension
        """
        self.path = ""
        self.save_file()
        
        
    def save_file(self):
        """
        Saving file to the path where getting from QFileDialog
        """
        fileobject = None
        if self.path is "":
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
            self.textEdit.document().setModified(False)
            self.setWindowTitle("%s - TextEditor" % 
                                QFileInfo(self.path).fileName())
        except (IOError, OSError), error:
            QMessageBox.warning(self, 
                                self.tr("TextEditor - Save Error"), 
                                self.tr("Unable to save {0}:{1}".format( 
                                self.path, error)))
            self.path = ""
        finally:
            if fileobject is not None:
                fileobject.close()
                
                
    def new_file(self):
        """
        To reset ui
        """
        self.ready_to_go()
        document = self.textEdit.document()
        document.clear()
        document.setModified(False)
        self.path = ""
        self.setWindowTitle(self.tr("unnamed - TextEditor"))
        
        
    def modified(self):
        """
        if document is modified then put a star
        Note: This function doesn't need :
        self.textEdit.document().setModified(True)
        """
        
        if self.path is "":
            self.setWindowTitle(self.tr("unnamed* - TextEditor"))
        else:
            self.setWindowTitle("%s* - TextEditor" % 
                                QFileInfo(self.path).fileName())
                               
def main():
    """
    loader function to start the application
    """
    app = QApplication(sys.argv)
    locale = QLocale.system().name()
    translator = QTranslator()
    translator.load("texteditor_%s.qm" % locale)
    app.installTranslator(translator)
    main_window = MainWindow()
    main_window.show()
    app.exec_()
    
if __name__ == "__main__":
    main()
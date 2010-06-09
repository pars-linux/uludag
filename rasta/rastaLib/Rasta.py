#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Rasta RST Editor
    2010 - Gökmen Göksel <gokmen:pardus.org.tr> """

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as Published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

# Python Core
import os
import sys

# Piksemel
try:
    import piksemel
except ImportError:
    sys.exit("Please install 'piksemel' package.")

# Docutils
try:
    import docutils.io
    import docutils.nodes
    from docutils.core import Publisher
    from StringIO import StringIO
except ImportError:
    sys.exit("Please install 'docutils' package.")

# PyQt4 Core Libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
try:
    from PyQt4.Qsci import QsciScintilla
except ImportError:
    sys.exit("Please install 'qscintilla2-python' package.")

# Rasta Core Library
try:
    from mainWindow import Ui_Rasta
except ImportError:
    sys.exit("Please run 'setup.py build' first.")

# RstLexer for Docutils
from rstLexer import RstLexer
from model import LogTableModel

TMPFILE = "/tmp/untitled.rst"

# Global Publisher for Docutils
PUB = Publisher(source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput)
PUB.set_reader('standalone', None, 'restructuredtext')
PUB.set_writer('html')
PUB.get_settings()
PUB.settings.halt_level = 7
PUB.settings.warning_stream = StringIO()

def clear_log(log):
    """ Removes not needed lines from log output """
    try:
        piks = piksemel.parseString(unicode(log))
        return piks.getAttribute("line"), piks.getTagData("paragraph")
    except:
        return 1,"Rasta parse error: %s" % log

class Rasta(QMainWindow):
    """ Rasta main class """

    def __init__(self, arguments):
        QMainWindow.__init__(self)
        self.ui = Ui_Rasta()
        self.ui.setupUi(self)

        # Toolbar
        self.ui.toolBar.addAction(self.ui.actionNew)
        self.ui.toolBar.addAction(self.ui.actionOpen)
        self.ui.toolBar.addAction(self.ui.actionSave)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionLive_Update)
        self.ui.toolBar.addAction(self.ui.actionUpdate_Now)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionUndo)
        self.ui.toolBar.addAction(self.ui.actionRedo)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionBold)
        self.ui.toolBar.addAction(self.ui.actionItalic)
        self.ui.toolBar.addAction(self.ui.actionCode)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionLink)
        self.ui.toolBar.addAction(self.ui.actionHeader)
        self.ui.toolBar.addSeparator()
        self.ui.toolBar.addAction(self.ui.actionAdd_Table)

        # Connections
        self.ui.actionOpen.triggered.connect(self.fileOpen)
        self.ui.actionSave.triggered.connect(self.saveFile)
        self.ui.actionSave_As.triggered.connect(self.saveFile)
        self.ui.actionNew.triggered.connect(self.newFile)
        self.ui.actionUpdate_Now.triggered.connect(self.updateRst)
        self.ui.actionShow_Logs.toggled.connect(self.toggleLogs)
        self.ui.actionBold.triggered.connect(self.editTrigger)
        self.ui.actionItalic.triggered.connect(self.editTrigger)
        self.ui.actionCode.triggered.connect(self.editTrigger)
        self.ui.actionHeader.triggered.connect(self.editTrigger)
        self.ui.actionLink.triggered.connect(self.editTrigger)
        self.ui.actionAdd_Table.triggered.connect(self.addTable)
        self.ui.actionRst_Howto.triggered.connect(self.showHelp)
        self.ui.actionSelect_Editor_Font.triggered.connect(self.showFontDialog)
        self.ui.actionAbout.triggered.connect(self.showAbout)
        self.ui.textEdit.textChanged.connect(self.updateRst)
        self.ui.logs.doubleClicked.connect(self.goToLine)

        # System settings
        self.settings = QSettings()
        self.readSettings()

        self.file_name = TMPFILE
        if "--hidesource" in arguments:
            self.ui.actionShow_Source.toggle()
        if len(arguments) > 1:
            if not unicode(arguments[1]).startswith("--"):
                self.loadFile(arguments[1])
                self.updateRst(force = True)
        else:
            self.showHelp()

    def buildSci(self, font = None):
        """ It builds QScintilla components """
        lexer = RstLexer(self.ui.textEdit, font)
        cfont = lexer.dfont
        font_metric = QFontMetrics(cfont)
        self.ui.textEdit.setLexer(lexer)
        self.ui.textEdit.setUtf8(True)
        self.ui.textEdit.setMarginLineNumbers(0, True)
        self.ui.textEdit.setMarginWidth(0, font_metric.width( "00000" ) + 5)
        self.ui.textEdit.setCaretLineVisible(True)
        self.ui.textEdit.setWrapMode(1)
        self.ui.textEdit.setFolding(True)
        self.ui.textEdit.setEdgeMode(QsciScintilla.EdgeLine)
        self.ui.textEdit.setEdgeColumn(80)
        self.ui.textEdit.setEdgeColor(QColor("#999"))
        self.ui.textEdit.markerDefine(QPixmap(":/icons/warning.png"), 31)
        self.ui.textEdit.setIndentationsUseTabs(False)
        self.ui.textEdit.setIndentationWidth(4)

    def showFontDialog(self):
        """ Show font selection dialog for QScintilla component """
        font = QFontDialog.getFont(self.ui.textEdit.lexer().dfont)[0]
        self.buildSci(font)

    def showAbout(self):
        """ Show About dialog """
        QMessageBox.about(self, "Rasta the Rst Editor", unicode(
                "Live view supported Qt4 based Webkit "
                "integrated Rst editor for Pardus Developers "
                "and all others. "
                "\n\nAuthor: Gökmen Göksel <gokmen@pardus.org.tr>", "UTF-8"))

    def addTable(self):
        """ Add Rst style table """
        editor = self.ui.textEdit
        editor.beginUndoAction()
        row = QInputDialog.getInteger(self, "Add Table", "Number of rows :")
        if row[1]:
            column = QInputDialog.getInteger(self, "Add Table", 
                    "Number of columns :")
            if column[1]:
                curline = editor.getCursorPosition()[0]
                editor.insert("\n")
                for times in range(row[0]):
                    editor.insert("%s+\n" % ("+-------" * column[0]))
                    editor.insert("%s|\n" % ("|       " * column[0]))
                editor.insert("%s+\n" % ("+-------" * column[0]))
        editor.endUndoAction()

    def editTrigger(self):
        """ If user clicks some of edit action it calls this method """
        marker = None
        pos_xx, pos_yy, pos_xy, pos_yz = self.ui.textEdit.getSelection()
        self.ui.textEdit.beginUndoAction()
        if self.sender() == self.ui.actionBold:
            marker = "**"
        elif self.sender() == self.ui.actionItalic:
            marker = "*"
        elif self.sender() == self.ui.actionCode:
            marker = "``"
        elif self.sender() == self.ui.actionHeader:
            self.ui.textEdit.insertAt("\n%s" % ("-" * (pos_yz-pos_yy)),
                                      pos_xy, pos_yz+1)
        elif self.sender() == self.ui.actionLink:
            link, res = QInputDialog.getText(self, "Insert Link", "Address :")
            if res:
                if not unicode(link[0]).startswith("http"):
                    link = "http://%s" % link
                self.ui.textEdit.insertAt("`", pos_xx, pos_yy)
                self.ui.textEdit.insertAt(" <%s>`_" % link, pos_xy, pos_yz + 1)
        if marker:
            self.ui.textEdit.insertAt(marker, pos_xx, pos_yy)
            self.ui.textEdit.insertAt(marker, pos_xy, pos_yz + len(marker))
        self.ui.textEdit.endUndoAction()

    def goToLine(self, index):
        """ Set cursor position to the given index """
        self.ui.textEdit.setFocus()
        self.ui.textEdit.setCursorPosition(
                index.child(index.row(),0).data().toInt()[0]-1,0)

    def toggleLogs(self, state):
        """ Show or Hide the log view """
        self.ui.Logs.setVisible(state)

    def showHelp(self):
        """ Show help for rst, it loads HELP document to the webview """
        _tmp = self.file_name
        if os.path.exists("/usr/share/rasta/HELP"):
            self.updateRst(
                    source = self.loadFile("/usr/share/rasta/HELP", 
                        parse_string = True))
        else:
            self.ui.webView.load(
                    QUrl("http://developer.pardus.org.tr/howto/howto-rst.html"))
        self.file_name = _tmp

    def newFile(self):
        """ Create new file """
        if self.checkModified():
            self.ui.textEdit.clear()
            self.file_name = TMPFILE

    def updateRst(self, source = None, force = False):
        """ Rebuild current source and show it in webview """
        if self.ui.actionLive_Update.isChecked() or\
                self.sender() == self.ui.actionUpdate_Now or\
                source or force:
            if not source:
                source = unicode(self.ui.textEdit.text())

            PUB.set_source(source)
            PUB.set_destination()
            PUB.document = PUB.reader.read(PUB.source, PUB.parser, PUB.settings)
            PUB.apply_transforms()

            logs = []
            self.ui.textEdit.markerDeleteAll(31)
            for node in PUB.document.traverse(docutils.nodes.problematic):
                node.parent.replace(node, node.children[0])
            for node in PUB.document.traverse(docutils.nodes.system_message):
                log = clear_log(node)
                node.parent.remove(node)
                logs.append(log)
                line = int(log[0])
                if self.ui.textEdit.lines() >= line:
                    self.ui.textEdit.markerAdd(line-1, 31)

            html = PUB.writer.write(PUB.document, PUB.destination)

            model = LogTableModel(logs, self)
            self.ui.logs.setModel(model)
            self.ui.logs.resizeColumnsToContents()
            self.ui.webView.setHtml(unicode(html, 'UTF-8'))
            if len(logs) > 0:
                self.ui.Logs.show()
            else:
                self.ui.Logs.hide()

    def checkModified(self):
        """ Checks if the document was modified and asks for saving """
        if (self.ui.textEdit.isModified()):
            ret = QMessageBox.warning(self, "Rasta",
                          "The document has been modified.\n"
                          "Do you want to save your changes?",
                          QMessageBox.Save |
                          QMessageBox.Discard |
                          QMessageBox.Cancel)
            if (ret == QMessageBox.Save):
                return self.saveFile()
            elif (ret == QMessageBox.Cancel):
                return False
        return True

    def fileOpen(self):
        """ It shows Open File dialog """
        if self.checkModified():
            file_name = QFileDialog.getOpenFileName(self)
            if (not file_name.isEmpty()):
                self.loadFile(file_name)

    def loadFile(self, file_name, parse_string=False):
        """ Load given file and show it in QSci component """
        file_object = QFile(file_name)
        if (not file_object.open(QFile.ReadOnly | QFile.Text)):
            QMessageBox.warning(self, "Rasta",
                                 QString("Cannot read file %1:\n%2.")
                                 .arg(file_name)
                                 .arg(file_object.errorString()))
            return
        self.file_name = file_name
        content = QTextStream(file_object)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        file_content = content.readAll()
        QApplication.restoreOverrideCursor()
        if parse_string:
            return unicode(file_content)
        self.ui.textEdit.setText(file_content)
        self.ui.textEdit.setModified(False)

    def saveFile(self):
        """ File save operation """
        if self.file_name == TMPFILE or self.sender() == self.ui.actionSave_As:
            get_new_file_name = QFileDialog.getSaveFileName(self, "Save File")
            if not get_new_file_name.isEmpty():
                self.file_name = get_new_file_name
            else:
                return
        file_object = QFile(self.file_name)
        if (not file_object.open(QFile.WriteOnly | QFile.Text)):
            QMessageBox.warning(self, "Rasta",
                                QString("Cannot write file %1:\n%2.")
                                .arg(self.file_name)
                                .arg(file_object.errorString()))
            return False

        # fileObject.write(self.ui.textEdit.text())
        out = QTextStream(file_object)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        out << self.ui.textEdit.text()
        QApplication.restoreOverrideCursor()
        self.ui.textEdit.setModified(False)
        return True

    def writeSettings(self):
        """ Write settings config file """

        # For MainWindow
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("liveupdate", 
                self.ui.actionLive_Update.isChecked())
        self.settings.setValue("showlogs", self.ui.actionShow_Logs.isChecked())
        self.settings.endGroup()

        # For TextEdit
        self.settings.beginGroup("TextEdit")
        self.settings.setValue("size", self.ui.textEdit.size())
        self.settings.setValue("font",
                                self.ui.textEdit.lexer().dfont.toString())
        self.settings.endGroup()

    def readSettings(self):
        """ Read settings from config file """

        # For MainWindow
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size", QSize(800, 400)).toSize())
        self.move(self.settings.value("pos", QPoint(20, 20)).toPoint())
        self.ui.actionLive_Update.setChecked(
                self.settings.value("liveupdate", True).toBool())
        self.ui.actionShow_Logs.setChecked(
                self.settings.value("showlogs", True).toBool())
        self.toggleLogs(self.ui.actionShow_Logs.isChecked())
        self.settings.endGroup()

        # For TextEdit
        self.settings.beginGroup("TextEdit")
        self.ui.textEdit.resize(
                self.settings.value("size", QSize(300, 560)).toSize())
        self.buildSci(self.settings.value('font', 'Droid Sans Mono'))
        self.settings.endGroup()

    def closeEvent(self, event):
        """ Catch close event to write settings before closing """
        self.writeSettings()
        if not self.checkModified():
            event.ignore()
            return
        event.accept()


#!/usr/bin/python
# -*- coding: utf-8 -*-

__version__ = "1.0"

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
    from docutils.core import publish_string
    import docutils.io, docutils.nodes
    from docutils.core import Publisher
    from docutils.parsers.rst.roles import _roles as docutils_roles
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
from rstLexer import RstLexer

TMPFILE = "/tmp/untitled.rst"

# Global Publisher for Docutils
pub = Publisher(source_class=docutils.io.StringInput,
        destination_class=docutils.io.StringOutput)
pub.set_reader('standalone', None, 'restructuredtext')
pub.set_writer('html')
pub.get_settings()
pub.settings.halt_level = 7
pub.settings.warning_stream = StringIO()

def clearLog(log):
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

        self.fileName = TMPFILE
        if "--hidesource" in arguments:
            self.ui.actionShow_Source.toggle()
        if len(arguments) > 1:
            if not unicode(arguments[1]).startswith("--"):
                self.loadFile(arguments[1])
                self.updateRst(force = True)
        else:
            self.showHelp()

    def buildSci(self, font = None):
        # QSci Settings
        lexer = RstLexer(self.ui.textEdit, font)
        cfont = lexer.dfont
        fontMetric = QFontMetrics(cfont)
        self.ui.textEdit.setLexer(lexer)
        self.ui.textEdit.setUtf8(True)
        self.ui.textEdit.setMarginLineNumbers(0, True)
        self.ui.textEdit.setMarginWidth(0, fontMetric.width( "00000" ) + 5)
        self.ui.textEdit.setCaretLineVisible(True)
        self.ui.textEdit.setWrapMode(1)
        self.ui.textEdit.setFolding(True)
        self.ui.textEdit.setEdgeMode(QsciScintilla.EdgeLine)
        self.ui.textEdit.setEdgeColumn(80)
        self.ui.textEdit.setEdgeColor(QColor("#999"))
        self.ui.textEdit.markerDefine(QPixmap(":/icons/warning.png"),31)

    def showFontDialog(self):
        font = QFontDialog.getFont(self.ui.textEdit.lexer().dfont)[0]
        self.buildSci(font)

    def showAbout(self):
        QMessageBox.about(self, "Rasta the Rst Editor", unicode(
                "Live view supported Qt4 based Webkit "
                "integrated Rst editor for Pardus Developers "
                "and all others. "
                "\n\nAuthor: Gökmen Göksel <gokmen@pardus.org.tr>"))

    def addTable(self):
        self.ui.textEdit.beginUndoAction()
        row = QInputDialog.getInteger(self, "Add Table", "Number of rows :")
        if row[1]:
            column = QInputDialog.getInteger(self, "Add Table", 
                    "Number of columns :")
            if column[1]:
                t = self.ui.textEdit
                curline = t.getCursorPosition()[0]
                t.insert("\n")
                for j in range(row[0]):
                    t.insert("%s+\n" % ("+-------" * column[0]))
                    t.insert("%s|\n" % ("|       " * column[0]))
                t.insert("%s+\n" % ("+-------" * column[0]))
        self.ui.textEdit.endUndoAction()

    def editTrigger(self):
        marker = None
        xx, yy, xy, yz = self.ui.textEdit.getSelection()
        self.ui.textEdit.beginUndoAction()
        if self.sender() == self.ui.actionBold:
            marker = "**"
        elif self.sender() == self.ui.actionItalic:
            marker = "*"
        elif self.sender() == self.ui.actionCode:
            marker = "``"
        elif self.sender() == self.ui.actionHeader:
            self.ui.textEdit.insertAt("\n%s" % ("-"*(yz-yy)),xy,yz+1)
        elif self.sender() == self.ui.actionLink:
            link, res = QInputDialog.getText(self, "Insert Link", "Address :")
            if res:
                if not unicode(link[0]).startswith("http"):
                    link = "http://%s" % link
                self.ui.textEdit.insertAt("`", xx, yy)
                self.ui.textEdit.insertAt(" <%s>`_" % link, xy, yz+1)
        if marker:
            self.ui.textEdit.insertAt(marker, xx, yy)
            self.ui.textEdit.insertAt(marker, xy, yz+len(marker))
        self.ui.textEdit.endUndoAction()

    def goToLine(self, index):
        self.ui.textEdit.setFocus()
        self.ui.textEdit.setCursorPosition(
                index.child(index.row(),0).data().toInt()[0]-1,0)

    def toggleLogs(self, state):
        self.ui.Logs.setVisible(state)

    def showHelp(self):
        _tmp = self.fileName
        if os.path.exists("/usr/share/rasta/HELP"):
            self.updateRst(
                    source = self.loadFile("/usr/share/rasta/HELP", 
                        parseString = True))
        else:
            self.ui.webView.load(
                    QUrl("http://developer.pardus.org.tr/howto/howto-rst.html"))
        self.fileName = _tmp

    def newFile(self):
        if self.checkModified():
            self.ui.textEdit.clear()
            self.fileName = TMPFILE

    def updateRst(self, source = None, force = False):
        if self.ui.actionLive_Update.isChecked() or\
                self.sender() == self.ui.actionUpdate_Now or\
                source or force:
            if not source:
                source = unicode(self.ui.textEdit.text())
            pub.set_source(source)
            pub.set_destination()
            pub.document = pub.reader.read(pub.source, pub.parser, pub.settings)
            pub.apply_transforms()

            logs = []
            self.ui.textEdit.markerDeleteAll(31)
            for node in pub.document.traverse(docutils.nodes.problematic):
                node.parent.replace(node, node.children[0])
            for node in pub.document.traverse(docutils.nodes.system_message):
                log = clearLog(node)
                node.parent.remove(node)
                logs.append(log)
                line = int(log[0])
                if self.ui.textEdit.lines() >= line:
                    self.ui.textEdit.markerAdd(line-1,31)

            html = pub.writer.write(pub.document, pub.destination)

            model = LogTableModel(logs, self)
            self.ui.logs.setModel(model)
            self.ui.logs.resizeColumnsToContents()
            self.ui.webView.setHtml(unicode(html))
            if len(logs) > 0:
                self.ui.Logs.show()
            else:
                self.ui.Logs.hide()

    def checkModified(self):
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
        if self.checkModified():
            fileName = QFileDialog.getOpenFileName(self)
            if (not fileName.isEmpty()):
                self.loadFile(fileName)

    def loadFile(self, fileName, parseString=False):
        fileObject = QFile(fileName)
        if (not fileObject.open(QFile.ReadOnly | QFile.Text)):
            QMessageBox.warning(self, "Rasta",
                                 QString("Cannot read file %1:\n%2.")
                                 .arg(fileName)
                                 .arg(fileObject.errorString()))
            return
        self.fileName = fileName
        content = QTextStream(fileObject)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        fileContent = content.readAll()
        QApplication.restoreOverrideCursor()
        if parseString:
            return unicode(fileContent)
        self.ui.textEdit.setText(fileContent)
        self.ui.textEdit.setModified(False)

    def saveFile(self):
        if self.fileName == TMPFILE or self.sender() == self.ui.actionSave_As:
            getNewFileName = QFileDialog.getSaveFileName(self, "Save File")
            if not getNewFileName.isEmpty():
                self.fileName = getNewFileName
            else:
                return
        fileObject = QFile(self.fileName)
        if (not fileObject.open(QFile.WriteOnly | QFile.Text)):
            QMessageBox.warning(this, "Rasta",
                                 QString("Cannot write file %1:\n%2.")
                                 .arg(fileName)
                                 .arg(file.errorString()));
            return False

        out = QTextStream(fileObject)
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
        self.settings.setValue("font", self.ui.textEdit.lexer().dfont.toString())
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

class LogTableModel(QAbstractTableModel):
    def __init__(self, logs, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = logs
        self.headerdata = ["Line", "Message"]

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.headerdata)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

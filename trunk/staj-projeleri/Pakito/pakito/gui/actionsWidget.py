# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

class ActionsWidget(QWidget):
    def __init__(self, parent, actionsFile = None):
        QWidget.__init__(self, parent)
        self.mainLayout = QVBoxLayout(self, 5, 5)
        self.mainLayout.setAutoAdd(True)
        self.change = False
        
        from editors import Editor as ed
        self.editor = ed("python", self)
        
        if actionsFile != None:
            self.editor.openFile(actionsFile)
        
    def changed(self):
        if not self.change:
            self.change = True
            self.emit(PYSIGNAL("changeName"), (True,))
        
    def fill(self, file):
        from os.path import abspath
        self.editor.openURL(KURL("file://%s" % abspath(file)))

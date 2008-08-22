 
# -*- coding: utf-8

from qt import *
from kdeui import *
from kdecore import *

class ComponentWidget(QWidget):
    def __init__(self, parent, componentFile = None):
        QWidget.__init__(self, parent)
        self.mainLayout = QVBoxLayout(self, 5, 5)
        self.mainLayout.setAutoAdd(True)
        self.change = False
        
        from editors import Editor as ed
        self.editor = ed("kwrite", self)
        
        if componentFile != None:
            self.editor.openFile(componentFile)
        
    def changed(self):
        if not self.change:
            self.change = True
            self.emit(PYSIGNAL("changeName"), (True,))
        
    def fill(self, file):
        from os.path import abspath
        self.editor.openURL(KURL("file://%s" % abspath(file)))

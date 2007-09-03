# -*- coding: utf-8 -*

from kio import KTrader
from kparts import createReadWritePart
from kdecore import KURL

from qt import *

class Editor(QWidget):
    def __init__(self, type, parent, file = None):
        QWidget.__init__(self, parent)
        mainLayout = QVBoxLayout(self)
        mainLayout.setAutoAdd(True)
        self.part = None
        self.editedFile = None
        
        # TODO: KTempFile
        if type == "python":
            offers = KTrader.self().query("application/x-python", "(Type == 'Service') and ('KParts/ReadWritePart' in ServiceTypes)")
        else:
            offers = KTrader.self().query("application/xml", "(Type == 'Service') and ('KParts/ReadWritePart' in ServiceTypes)")
            
        #select first part
        for ptr in offers:
            part = createReadWritePart(ptr.library(), self, ptr.name())#, "KTextEditor.Document")
            if part:
                self.part = part
                break
#        view = part.createView(self, 0)
            
        if file != None:
            self.openFile(file)
    
    def getContent(self):
        url = self.part.url()
        
        if (url == None or url == ""):
            return None
        
        self.part.save()
        temp = open(self.editedFile)
        content = unicode(temp.read())
        temp.close()
        return content
    
    def save(self):
        self.part.save()
    
    def saveAs(self):
        pass

    def openFile(self, file):
        from os.path import abspath
        self.part.openURL(KURL("file://%s" % abspath(file)))
        self.editedFile = abspath(file)
        

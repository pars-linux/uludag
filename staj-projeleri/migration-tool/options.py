# -*- coding: utf-8 -*-

from qt import *

class Options(QWidget):
    def __init__(self, sources):
        self.options = {}
        QWidget.__init__(self)
        self.layout = QVBoxLayout(self)
        
        # Bookmarks:
        if sources.has_key("Firefox Profile Path") or sources.has_key("Favorites Path"):
            self.options["Bookmarks"] = True
            self.Bookmarks = QGroupBox(self)
            self.Bookmarks.setTitle(u"Yer İmleri")
            self.Bookmarks.setColumnLayout(0,Qt.Vertical)
            self.BookmarksLayout = QVBoxLayout(self.Bookmarks.layout())
            self.layout.addWidget(self.Bookmarks)
            
            if sources.has_key("Firefox Profile Path"):
                self.options["FFBookmarks"] = False
                self.FFBookmarks = QCheckBox(self.Bookmarks)
                self.FFBookmarks.setText(u"Firefox yer imlerini alayım mı?")
                self.BookmarksLayout.addWidget(self.FFBookmarks)
                self.connect(self.FFBookmarks, SIGNAL("toggled(bool)"), self.changeFFBookmarks)
            
            if sources.has_key("Favorites Path"):
                self.options["IEBookmarks"] = False
                self.IEBookmarks = QCheckBox(self.Bookmarks)
                self.IEBookmarks.setText(u"Internet Explorer yer imlerini alayım mı?")
                self.BookmarksLayout.addWidget(self.IEBookmarks)
                self.connect(self.IEBookmarks, SIGNAL("toggled(bool)"), self.changeIEBookmarks)
        spacer = QSpacerItem(1,1,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout.addItem(spacer)
    
    def changeFFBookmarks(self, value):
        self.options["FFBookmarks"] = value
    
    def changeIEBookmarks(self, value):
        self.options["IEBookmarks"] = value

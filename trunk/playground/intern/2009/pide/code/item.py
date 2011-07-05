# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4.kdeui import KIcon

# UI
from ui_item import Ui_ItemWidget

# Sender
from sender import FileSender

class ItemListWidgetItem(QtGui.QListWidgetItem):
    def __init__(self, parent, widget):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.widget = widget
        self.setSizeHint(QtCore.QSize(300, 48))

    def getId(self):
        return self.widget.getId()

    def getType(self):
        return self.widget.getType()


class ItemWidget(QtGui.QWidget, Ui_ItemWidget):
    def __init__(self, name, address):
        QtGui.QListWidgetItem.__init__(self)
        self.setupUi(self)

        self.setTitle(name)
        self.setDescription(address)
        self.connect(self.sendButton, QtCore.SIGNAL("clicked()"), self.connectReceiver)

    def setTitle(self, title):
        self.labelTitle.setText(unicode(title))

    def setDescription(self, description):
        self.labelDescription.setText(unicode(description))

    def connectReceiver(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if filename:
            self.instance = FileSender(filename, unicode(self.labelDescription.text()))
            self.instance.start()


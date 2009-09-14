# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4.kdeui import KIcon

# UI
from ui_item import Ui_ItemWidget


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

    def mouseDoubleClickEvent(self, event):
        self.pushEdit.animateClick(100)

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def setTitle(self, title):
        self.labelTitle.setText(unicode(title))

    def getTitle(self):
        return unicode(self.labelTitle.text())

    def setDescription(self, description):
        self.labelDescription.setText(unicode(description))

    def getDescription(self):
        return unicode(self.labelDescription.text())

    def setIcon(self, icon):
        self.labelIcon.setPixmap(icon.pixmap(32, 32))

    def getState(self):
        return self.checkState.checkState()

    def setState(self, state):
        if state == True:
            state = QtCore.Qt.Checked
        elif state == False:
            state = QtCore.Qt.Unchecked
        return self.checkState.setCheckState(state)

    def hideEdit(self):
        self.pushEdit.hide()

    def hideDelete(self):
        self.pushDelete.hide()

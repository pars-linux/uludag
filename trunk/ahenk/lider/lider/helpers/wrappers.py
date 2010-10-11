#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Wrappers for UI widgets
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore


# Helper modules
from lider.helpers import decorators


#@decorators.cache
def Image(icon_name, size=32):
    """
        Creates a QImage object from given resource, also scales it.

        Arguments:
            icon_name: Name of an image resource without file suffix.
            size: Icon size
        Returns: QImage object
    """
    pixmap = QtGui.QPixmap(":/icons/%s.png" % icon_name)
    return QtGui.QImage(pixmap.scaled(QtCore.QSize(size, size), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))

#@decorators.cache
def Icon(icon_name, size=32, overlays=[]):
    """
        Creates an icon.

        Arguments:
            icon_name: Name of an image resource without file suffix.
            size: Icon size
            overlays: List of overlay icons in (name, x, y) format
        Returns: QIcon object
    """
    # Load main icon
    image = Image(icon_name, size)

    # Create new paper
    pixmap = QtGui.QPixmap(size, size)
    pixmap.fill(QtGui.QColor(255, 255, 255, 0))

    # Create a painter
    painter = QtGui.QPainter(pixmap)
    painter.setBackgroundMode(QtCore.Qt.TransparentMode)

    # Draw main icon
    painter.drawImage(QtCore.QRect(0, 0, size, size), image, QtCore.QRect(0, 0, image.width(), image.height()))

    # Draw overlay icons
    for ext_name, ext_x, ext_y in overlays:
        # Set overlay icon size
        ext_size = size / 4
        # Load extension icon
        ext_image = Image(ext_name, ext_size)
        # Calculate coordinates to draw overlay icon
        ext_rect = QtCore.QRect((image.width() - ext_size) * ext_x, (image.height() - ext_size) * ext_y, ext_size, ext_size)
        # Draw overlay icon
        painter.drawImage(ext_rect, ext_image, QtCore.QRect(0, 0, ext_image.width(), ext_image.height()))

    # End drawing
    painter.end()

    # Add pixmap to QIcon
    icon = QtGui.QIcon()
    icon.addPixmap(pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)

    return icon

def TreeNode(parent, name, icon_name):
    """
        Creates an QTreeWidget item.

        Arguments:
            parent: Parent item
            name: Label
            icon_name: Name of an image resource without file suffix.
        Returns: QTreeWidgetItem object
    """
    node = QtGui.QTreeWidgetItem(parent)
    node.name = name
    node.setText(0, name)

    icon = Icon(icon_name)
    node.setIcon(0, icon)

    return node

class Menu(QtGui.QMenu):
    """
        QMenu wrapper for creating popups without pain.

        Usage:
            menu = Menu()
            menu.newAction("Item 1", "green_led", self.slotItem1Clicked)
    """

    def __init__(self, parent):
        """
            Constructor for Menu class.

            Arguments:
                parent: Parent object
        """
        QtGui.QMenu.__init__(self, parent)
        self.parent = parent

    def newAction(self, label, icon, slot):
        """
            Adds new action to menu.

            Arguments:
                label: Item label
                icon: QIcon object
                slot: Function to be executed when item is triggered.
            Returns: QAction object
        """
        action = self.addAction(icon, label)
        self.parent.connect(action, QtCore.SIGNAL("triggered(bool)"), slot);
        return action

class Progress:
    """
        Progress dialog.

        Usage:
            progress = Progress(self)
            progress.started("Message")
            progress.progress("Loading", 50)
            progress.progress("Loading", 100)
            progress.finished()
    """

    def __init__(self, parent):
        """
            Constructor for Progress class.

            Arguments:
                parent: Parent object
        """
        self.parent = parent
        self.dialog = None

    def started(self, title):
        """
            Starts progress dialog.

            Arguments:
                title: Dialog title
        """
        self.dialog = QtGui.QProgressDialog(title, "Stop", 0, 0, self.parent)
        self.dialog.setCancelButton(None)
        self.dialog.show()
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)

    def progress(self, msg, percent):
        """
            Updates progress percentage.

            Arguments:
                msg: Dialog message
                percentage: Progress
        """
        self.dialog.setLabelText(msg)
        if percent < 100:
            self.dialog.setValue(percent)
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)

    def finished(self):
        """
            Closes progress dialog.
        """
        if self.dialog:
            self.dialog.done(0)
        self.dialog = None

#!/usr/bin/python
    
# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext
    
# Import header that specifies notification class
from notification import *

# Import PyQt4 GUI stuff:
from PyQt4 import QtGui
from PyQt4 import QtCore

class NotificationTrayIcon(QtGui.QSystemTrayIcon):
    def __init__(self, notification_displayer, icon = None, parent = None):
        if icon == None:
            QtGui.QSystemTrayIcon.__init__(self,  parent)
        else:
            QtGui.QSystemTrayIcon.__init__(self,  icon, parent)
        self.BuildMenu()
        self.show()
        self.notification_displayer = notification_displayer
    
    def Die(self):
        quit()
    
    def BuildMenu(self):
        self.menu = QtGui.QMenu()
        self.action = QtGui.QAction(_("Exit"), self.menu)
        self.menu.addAction(self.action)
        self.connect(self.action,  QtCore.SIGNAL("triggered()"),  self.Die)
        self.setContextMenu(self.menu)
    
    def DisplayNotification(self, notif):
        if isinstance(notif,  Notification) == True:
            self.showMessage(_("Notification arrived!"),  notif.text)
        else:
            self.showMessage(_("Error"),  _("Typing error, this program has just bought the farm."))

class NotificationDisplayer:
    def __init__(self):
        self.tray_icon = NotificationTrayIcon(self,  QtGui.QIcon("icon.png"))

    def DisplayNotification(self, notif):
        self.tray_icon.DisplayNotification(notif)

# -*- coding: utf-8 -*-
#
#!/usr/bin/python
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import gettext
__trans = gettext.translation('gtk-kde4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtCore, QtGui
from gui import Ui_GtkKde4

THEMES_ROOT= "/usr/share/themes"
ICONS_ROOT = "/usr/share/icons"
GTKRC_PATH = os.path.join(os.getenv("HOME"),".kde4/share/config/gtkrc-2.0")
KDE4_THEME = "gtk-qt4"

GTKRC_TEMPLATE = """# Added by Gtk-Kde4 don't edit manually.
include "%(theme_path)s"
gtk-theme-name="%(theme_name)s"
gtk-font-name="%(font)s"
gtk-icon-theme-name="%(icon_theme)s"
"""

class GtkKde4(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, None)
        self.ui = Ui_GtkKde4()
        self.ui.setupUi(self)

        self.getCurrentSettings()
        self.fillThemes()
        self.fillIcons()

        self.connect(self.ui.changeStyle, QtCore.SIGNAL("clicked()"), self.saveChanges)

    def getCurrentSettings(self):
        conf = open(GTKRC_PATH)
        self.currentTheme = ""
        self.currentIconTheme = ""
        for line in conf.readlines():
            if line.startswith("gtk-theme-name"):
                self.currentTheme = line.split("=")[1].strip("\"\n")
            if line.startswith("gtk-font-name"):
                currentFont = line.split("=")[1].strip("\"\n").split()
                self.ui.fontSize.setValue(int(currentFont[len(currentFont) - 1]))
                currentFont.pop()
                self.ui.fontType.setCurrentFont(QtGui.QFont(" ".join(currentFont)))
            if line.startswith("gtk-icon-theme-name"):
                self.currentIconTheme = line.split("=")[1].strip("\"\n")

    def fillThemes(self):
        index = 0
        self.ui.styleBox.clear()
        for theme in os.listdir(THEMES_ROOT):
            if os.path.exists(os.path.join(THEMES_ROOT, theme, "gtk-2.0/gtkrc")):
                if theme==KDE4_THEME:
                    self.ui.styleBox.addItem(_("Kde 4 Default Theme"),QtCore.QVariant(theme))
                else:
                    self.ui.styleBox.addItem(theme,QtCore.QVariant(theme))
                if theme==self.currentTheme:
                    index = self.ui.styleBox.count()
        self.ui.styleBox.setCurrentIndex(index-1)

    def fillIcons(self):
        index = 0
        self.ui.iconBox.clear()
        for icons in os.listdir(ICONS_ROOT):
            if os.path.exists(os.path.join(ICONS_ROOT,icons,"index.theme")):
                self.ui.iconBox.addItem(icons)
                if icons == self.currentIconTheme:
                    index = self.ui.iconBox.count()
        self.ui.iconBox.setCurrentIndex(index-1)

    def saveChanges(self):
        conf = file(GTKRC_PATH,"w")
        settings = {}
        selectedTheme = str(self.ui.styleBox.itemData(self.ui.styleBox.currentIndex()).toString())
        settings["theme_path"] = os.path.join(THEMES_ROOT, selectedTheme, "gtk-2.0/gtkrc")
        settings["theme_name"] = selectedTheme
        settings["icon_theme"] = str(self.ui.iconBox.currentText())
        settings["font"] = "%s %s" % (str(self.ui.fontType.currentText()), str(self.ui.fontSize.value()))
        conf.write(GTKRC_TEMPLATE % settings)
        conf.close()
        QtGui.QMessageBox(QtGui.QMessageBox.Information, _("GTK-Kde4"), _("Config file saved. You need to restart running GTK Applications to see changes.")).exec_()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    gui = GtkKde4()
    gui.show()
    sys.exit(app.exec_())


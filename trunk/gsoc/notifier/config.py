#!/usr/bin/python

import sys
    
# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext

# Import PyQt4 GUI stuff:
from PyQt4 import QtCore, QtGui, uic

class Configurator:
	def __init__(self):
		self.Initialize()

	def Initialize(self):
		# Load the GUI:
		self.ui_class, self.base_class = uic.loadUiType("ui/configurator.ui")
		self.configUI = self.MakeConfigUIClass()
		self.configWindow = self.configUI()

	def Display(self):
		self.configWindow.show()

	def MakeConfigUIClass(self_outer):
		class ConfigUI(self_outer.ui_class, self_outer.base_class):
			def __init__(self):
				# Set up the UI read from the .ui file:
				self_outer.ui_class.__init__(self)
				self_outer.base_class.__init__(self)

				self.setupUi(self)

				self.current_file = None

				QtCore.QObject.connect(self.browse_skin_path, QtCore.SIGNAL("clicked()"), self.BrowseSkinFiles)
				QtCore.QObject.connect(self.open_conf_file, QtCore.SIGNAL("triggered()"), self.BrowseConfFiles)

			def BrowseConfFiles(self):
				file_dialog = QtGui.QFileDialog(self, _("Choose a configuration file (.xml)"))
				file_dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
				QtCore.QObject.connect(file_dialog, QtCore.SIGNAL("filesSelected(const QStringList&)"), self.ImportConfFile)
				file_dialog.show()

			def BrowseSkinFiles(self):
				file_dialog = QtGui.QFileDialog(self, _("Choose a skin file (.ui)"))
				file_dialog.setFileMode(QtGui.QFileDialog.ExistingFile)
				QtCore.QObject.connect(file_dialog, QtCore.SIGNAL("filesSelected(const QStringList&)"), self.SetSkinPath)
				file_dialog.show()

			def SetSkinPath(self, file_list):
				if file_list.__len__() != 0:
					self.skin_path.setText(file_list[0])

			def ImportConfFile(self, file_list):
				return

			def Destroy(self):
				self.deleteLater()

		return ConfigUI

# If executed as the main program:
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	config_window = Configurator()
	config_window.Display()
	sys.exit(app.exec_())
else:
	print _("This program is not meant to be loaded as a module.")

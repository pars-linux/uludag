#!/usr/bin/python

import sys
    
# Import internationalization support:
import gettext
_ = gettext.translation("notman", "./i18n", fallback = True).ugettext

# Import PyQt4 GUI stuff:
from PyQt4 import QtCore, QtGui, uic

class SampleFrame(QtGui.QFrame):
	def __init__(self, configurator):
		QtGui.QFrame.__init__(self)
		self.configurator = configurator
	
	def moveEvent(self, move_event):
		self.configurator.startx.setText(self.configurator.aux_frame.geometry().x().__str__())
		self.configurator.starty.setText(self.configurator.aux_frame.geometry().y().__str__())

	def resizeEvent(self, resize_event):
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.configurator.percent_width.setText(((100 * resize_event.size().width() / screen.width())).__str__())
		self.configurator.percent_height.setText(((100 * resize_event.size().height() / screen.height())).__str__())

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

				# Create the auxillary window used for manual positioning:
				self.aux_frame = SampleFrame(self)
				self.aux_frame.setWindowTitle("Sample Notification")
				layout = QtGui.QHBoxLayout(self.aux_frame)
				description_label = QtGui.QLabel("Move this window on the screen to choose your preferred starting point.", self.aux_frame)
				layout.addWidget(description_label)
				description_label.setWordWrap(True)
				self.aux_frame.resize(280, 120)
				self.aux_frame.move(400, 300)
				
				# Attach relevant signals to slots:

				# Signals used for quitting the application:
				QtCore.QObject.connect(self.discard_button, QtCore.SIGNAL("clicked()"), self.Destroy)
				QtCore.QObject.connect(self.quit_configurator, QtCore.SIGNAL("triggered()"), self.Destroy)

				# Signals for choosing files:
				QtCore.QObject.connect(self.browse_skin_path, QtCore.SIGNAL("clicked()"), self.BrowseSkinFiles)
				QtCore.QObject.connect(self.open_conf_file, QtCore.SIGNAL("triggered()"), self.BrowseConfigFiles)

				# Signal for showing the auxillary window:
				QtCore.QObject.connect(self.manual_position, QtCore.SIGNAL("toggled(bool)"), self.ShowAuxWindow)

				# Signals for reflecting the changes on the inputs:
				QtCore.QObject.connect(self.animation_time, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.lifetime, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.time_quanta, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.percent_height, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.percent_width, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.startx, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.starty, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.skin_path, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)

			def UpdateLooks(self):
				# Adjust the size of the auxillary window to reflect the notification window size:
				screen = QtGui.QDesktopWidget().screenGeometry()
				pixel_width = self.aux_frame.width()
				pixel_height = self.aux_frame.height()
				aux_frame_x = self.aux_frame.x()
				aux_frame_y = self.aux_frame.y()
				if self.percent_width.text() != "":
					pixel_width = int(self.percent_width.text()) * screen.width() / 100
				if self.percent_height.text() != "":
					pixel_height = int(self.percent_height.text()) * screen.height() / 100
				if self.startx.text() != "":
					aux_frame_x = int(self.startx.text()) - (self.aux_frame.geometry().x() - self.aux_frame.x())
				if self.starty.text() != "":
					aux_frame_y = int(self.starty.text()) - (self.aux_frame.geometry().y() - self.aux_frame.y())
				self.aux_frame.resize(pixel_width, pixel_height)
				self.aux_frame.move(aux_frame_x, aux_frame_y)

			def ShowAuxWindow(self, isChecked):
				if isChecked:
					aux_frame_x = self.aux_frame.x()
					aux_frame_y = self.aux_frame.y()
					if self.startx.text() != "" and self.starty.text() != "":
						aux_frame_x = int(self.startx.text()) - (self.aux_frame.geometry().x() - self.aux_frame.x())
						aux_frame_y = int(self.starty.text()) - (self.aux_frame.geometry().y() - self.aux_frame.y())
					self.aux_frame.move(aux_frame_x, aux_frame_y)
					self.aux_frame.show()
				else:
					self.aux_frame.hide()

			def BrowseConfigFiles(self):
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
				self.percent_width.setText("17")
				self.percent_height.setText("13")
				self.UpdateLooks()
				return

			def Destroy(self):
				quit()

		return ConfigUI

# If executed as the main program:
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	config_window = Configurator()
	config_window.Display()
	sys.exit(app.exec_())
else:
	print _("This program is not meant to be loaded as a module.")

#!/usr/bin/env python

import sys
import os
import shutil
from distutils.spawn import find_executable
import py_compile
    
# Import internationalization support:
import gettext
_ = gettext.translation("notman", fallback = True).ugettext

# Import PyQt4 GUI stuff:
from PyQt4 import QtCore, QtGui
from PyQt4 import pyqtconfig

# Import our own GUI stuff:
from pnm.ui.configurator import Ui_MainWindow

# Import XML stuff:
from lxml import etree

# XSD path:
xsd_path = "/usr/share/pnm/pnm.xsd"

# For compiling skin files (.ui files) and adding gettext support to them:
def py_file_name(ui_file):
	return os.path.splitext(ui_file)[0] + '.py'

def add_gettext_support(ui_file):
	# hacky, too hacky. but works...
	py_file = py_file_name(ui_file)
	# lines in reverse order
	lines =  ["\n_ = gettext.translation(\"notman\", fallback = True).ugettext", "\nimport gettext"]
	f = open(py_file, "r").readlines()
	for l in lines:
		f.insert(1, l)
	x = open(py_file, "w")
	keyStart = "QtGui.QApplication.translate"
	keyEnd = ", None, QtGui.QApplication.UnicodeUTF8)"
	styleKey = "setStyleSheet"
	for l in f:
		if not l.find(keyStart)==-1 and l.find(styleKey)==-1:
			z = "%s(_(" % l.split("(")[0]
			y = l.split(",")[0]+', '
			l = l.replace(y,z)
		l = l.replace(keyEnd,")")
		x.write(l)

def compile_ui(ui_file):
	pyqt_configuration = pyqtconfig.Configuration()
	pyuic_exe = find_executable('pyuic4', pyqt_configuration.default_bin_dir)
	if not pyuic_exe:
		# Search on the $Path.
		pyuic_exe = find_executable('pyuic4')
	cmd = [pyuic_exe, ui_file, '-o']
	cmd.append(py_file_name(ui_file))
	os.system(' '.join(cmd))

def ValidateXMLTree(xml_tree):
	schema = etree.XMLSchema(etree.parse(xsd_path))
	if schema.validate(xml_tree):
		return (xml_tree, True)
	else:
		return (schema.error_log.last_error, False)

def ValidateAndParseXML(file_name):
	schema = etree.XMLSchema(etree.parse(xsd_path))
	try:
		xml_doc = etree.parse(file_name)
	except Exception, err:
		return (err, False)
	if schema.validate(xml_doc):
		return (xml_doc, True)
	else:
		return (schema.error_log.last_error, False)

class SampleFrame(QtGui.QFrame):
	def __init__(self, configurator, window_flags):
		QtGui.QFrame.__init__(self, None, window_flags)
		self.configurator = configurator
		self.moving = False
		self.resizing = False
		self.startx = 0
		self.starty = 0
	
	def mousePressEvent(self, press_event):
		if press_event.button() == QtCore.Qt.LeftButton:
			self.moving = True
			self.startx = press_event.x()
			self.starty = press_event.y()
		if press_event.button() == QtCore.Qt.RightButton:
			self.resizing = True
			self.basex = self.width() - press_event.globalX()
			self.basey = self.height() - press_event.globalY()

	def mouseReleaseEvent(self, release_event):
		if release_event.button() == QtCore.Qt.LeftButton:
			self.moving = False
		if release_event.button() == QtCore.Qt.RightButton:
			self.resizing = False

	def mouseMoveEvent(self, move_event):
		if self.moving == True:
			self.move(move_event.globalX() - self.startx, move_event.globalY() - self.starty)
		if self.resizing == True:
			self.resize(self.basex + move_event.globalX(), self.basey + move_event.globalY())

	def moveEvent(self, move_event):
		self.configurator.startx.setText(move_event.pos().x().__str__())
		self.configurator.starty.setText(move_event.pos().y().__str__())

	def resizeEvent(self, resize_event):
		screen = QtGui.QDesktopWidget().screenGeometry()
		self.configurator.percent_width.setText(((100 * resize_event.size().width() / screen.width())).__str__())
		self.configurator.percent_height.setText(((100 * resize_event.size().height() / screen.height())).__str__())

class Configurator:
	def __init__(self, config_file):
		self.Initialize(config_file)

	def Initialize(self, config_file):
		# Load the GUI:
		self.ui_class, self.base_class = Ui_MainWindow, QtGui.QMainWindow
		self.configUI = self.MakeConfigUIClass()
		self.configWindow = self.configUI(config_file)

	def Display(self):
		self.configWindow.show()

	def MakeConfigUIClass(self_outer):
		class ConfigUI(self_outer.ui_class, self_outer.base_class):
			def __init__(self, config_file):
				# Set up the UI read from the .ui file:
				self_outer.ui_class.__init__(self)
				self_outer.base_class.__init__(self)

				self.setupUi(self)

				self.current_file = config_file

				# Create the auxillary window used for manual positioning:
				wflags = QtCore.Qt.WindowFlags() | QtCore.Qt.X11BypassWindowManagerHint | QtCore.Qt.WindowStaysOnTopHint
				self.aux_frame = SampleFrame(self, wflags)
				self.aux_frame.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
				self.aux_frame.setLineWidth(1)
				self.aux_frame.setMidLineWidth(1)
				self.aux_frame_xcoord = 400
				self.aux_frame_ycoord = 300
				layout = QtGui.QHBoxLayout(self.aux_frame)
				description_label = QtGui.QLabel(_("Move this window on the screen to choose your preferred starting point."), self.aux_frame)
				layout.addWidget(description_label)
				description_label.setWordWrap(True)
				
				# Attach relevant signals to slots:

				# Signals used for quitting the application:
				QtCore.QObject.connect(self.discard_button, QtCore.SIGNAL("clicked()"), self.Destroy)
				QtCore.QObject.connect(self.save_button, QtCore.SIGNAL("clicked()"), self.Save)
				QtCore.QObject.connect(self.quit_configurator, QtCore.SIGNAL("triggered()"), self.Destroy)
				QtCore.QObject.connect(self.save_conf_file, QtCore.SIGNAL("triggered()"), self.Save)

				# Signals for choosing files:
				QtCore.QObject.connect(self.browse_skin_path, QtCore.SIGNAL("clicked()"), self.BrowseSkinFiles)
				QtCore.QObject.connect(self.open_conf_file, QtCore.SIGNAL("triggered()"), self.BrowseConfigFiles)

				# Signal for showing the auxillary window:
				QtCore.QObject.connect(self.manual_position, QtCore.SIGNAL("toggled(bool)"), self.ShowAuxWindow)

				# Signals for reflecting the changes on the inputs:
				QtCore.QObject.connect(self.percent_height, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.percent_width, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.startx, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)
				QtCore.QObject.connect(self.starty, QtCore.SIGNAL("editingFinished()"), self.UpdateLooks)

				# Import the config file to fill in the form:
				self.ImportConfFile([self.current_file])

			def UpdateLooks(self):
				# Adjust the size of the auxillary window to reflect the notification window size:
				screen = QtGui.QDesktopWidget().screenGeometry()
				pixel_width = self.aux_frame.width()
				pixel_height = self.aux_frame.height()
				aux_frame_x = self.aux_frame_xcoord
				aux_frame_y = self.aux_frame_ycoord
				if self.percent_width.text() != "":
					pixel_width = int(self.percent_width.text()) * screen.width() / 100
				if self.percent_height.text() != "":
					pixel_height = int(self.percent_height.text()) * screen.height() / 100
				if self.startx.text() != "":
					aux_frame_x = int(self.startx.text())
				if self.starty.text() != "":
					aux_frame_y = int(self.starty.text())
				self.aux_frame.resize(pixel_width, pixel_height)
				self.aux_frame.move(aux_frame_x, aux_frame_y)

			def ShowAuxWindow(self, isChecked):
				if isChecked:
					self.UpdateLooks()
					self.aux_frame.show()
				else:
					self.aux_frame_xcoord = self.aux_frame.x()
					self.aux_frame_ycoord = self.aux_frame.y()
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

			def Save(self):
					# Check to see if the .notify directory exists in the users home directory:
					if not os.path.exists(os.path.join(os.path.expanduser("~"), ".notify")):
						# If it doesn't exist, create the directory:
						os.mkdir(os.path.join(os.path.expanduser("~"), ".notify"))
					
					if self.current_file == None:
						message_box = QtGui.QMessageBox(self)
						message_box.setWindowTitle(_("No current configuration file found"))
						message_box.setText(_("You need to open a configuration file first."))
						message_box.exec_()
						return None
					
					message_box = QtGui.QMessageBox(self)
					message_box.setWindowTitle(_("Saving Confirmation"))
					message_box.setText(_("Are you sure you want to overwrite the configuration file?"))
					message_box.addButton(QtGui.QMessageBox.Cancel)
					message_box.addButton(QtGui.QMessageBox.Ok)
					result = message_box.exec_()
					if result == QtGui.QMessageBox.Cancel:
						return None
					
					# Construct the XML tree:
					root = etree.Element("pnmconfig")

					geometry = etree.SubElement(root, "geometry")
					height = etree.SubElement(geometry, "height")
					height.text = self.percent_height.text().__str__()
					width = etree.SubElement(geometry, "width")
					width.text = self.percent_width.text().__str__()

					manager = etree.SubElement(root, "manager")
					lifetime = etree.SubElement(manager, "lifetime")
					lifetime.text = self.manager_lifetime.text().__str__()

					direction = etree.SubElement(root, "direction")
					if self.stacking_down.isChecked():
						direction.attrib["choice"] = "down"
					else:
						direction.attrib["choice"] = "up"

					skinpath = etree.SubElement(root, "skinpath")
					skinpath.text = self.skin_path.text().__str__()
					# Also compile the UI file into a py file and add it to pnm.ui
					# Note that the UI file needs to supply the class Ui_mainwindow.
					if skinpath.text != "default":
						try:
							compile_ui(skinpath.text)
							add_gettext_support(skinpath.text)
							if not os.path.exists(os.path.join(os.path.expanduser("~"), ".notify/pnmskins")):
								os.mkdir(os.path.join(os.path.expanduser("~"), ".notify/pnmskins"))
							# Now we are sure that we have the ~/.notify/pnmskins directory, move the result there:
							shutil.move(py_file_name(skinpath.text), os.path.join(os.path.join(os.path.expanduser("~"), ".notify"), "pnmskins"))
							py_compile.compile(os.path.join(os.path.join(os.path.join(os.path.expanduser("~"), ".notify"), "pnmskins"), os.path.basename(py_file_name(skinpath.text))))
						except:
							message_box = QtGui.QMessageBox(self)
							message_box.setWindowTitle(_("Error in reading or compiling the skin file"))
							message_box.setText(_("The skin file you supplied can not be used. The reason may be one of the following: Either the file couldn't be read, or it couldn't be compiled, or you don't have the required permissions."))
							message_box.exec_()
							skinpath.text = "default"
							return None						

					position = etree.SubElement(root, "position")
					if self.manual_position.isChecked() == True:
						position.attrib["choice"] = "manual"
						xcoord = etree.SubElement(position, "xcoord")
						xcoord.text = self.startx.text().__str__()
						ycoord = etree.SubElement(position, "ycoord")
						ycoord.text = self.starty.text().__str__()
					elif self.upper_right_radio.isChecked() == True:
						position.attrib["choice"] = "upperRight"
					else:
						position.attrib["choice"] = "lowerRight"

					animation = etree.SubElement(root, "animation")
					totaltime = etree.SubElement(animation, "totaltime")
					totaltime.text = self.animation_time.text().__str__()
					timequanta = etree.SubElement(animation, "timequanta")
					timequanta.text = self.time_quanta.text().__str__()
					windowlifetime = etree.SubElement(animation, "windowlifetime")
					windowlifetime.text = self.lifetime.text().__str__()

					result, isValid = ValidateXMLTree(root)
					if isValid == True:
						# The resultant XML tree is valid, save the XML file:
						try:
							open(self.current_file, "w").write(etree.tostring(root, pretty_print = True))
						except:
							message_box = QtGui.QMessageBox(self)
							message_box.setWindowTitle(_("Error in saving XML file"))
							message_box.setText(_("Couldn't write back to the opened file, check permissions."))
							message_box.exec_()
						# If there is no existing ~/.notify/config.xml, ask if the user wants to make this file the config file to be used:
						if not os.path.exists(os.path.join(os.path.expanduser("~"), ".notify/config.xml")):
							message_box = QtGui.QMessageBox(self)
							message_box.setWindowTitle(_("No currently used config file found"))
							message_box.setText(_("Do you want to make this file the currently used config file?"))
							message_box.addButton(QtGui.QMessageBox.Cancel)
							message_box.addButton(QtGui.QMessageBox.Ok)
							result = message_box.exec_()
							if result == QtGui.QMessageBox.Ok:
								open(os.path.join(os.path.expanduser("~"), ".notify/config.xml"), "w").write(etree.tostring(root, pretty_print = True))
						return True
					else:
						message_box = QtGui.QMessageBox(self)
						message_box.setWindowTitle(_("Error in saving XML file"))
						message_box.setText(_("You entered an illegal value.\nXSD Validation Error:\n%s" % result))
						message_box.exec_()
						return None

			def ImportConfFile(self, file_list):
				# Try to validate the XML file:
				result, isValid = ValidateAndParseXML(file_list[0].__str__())
				# If the file is valid, update the GUI accordingly:
				if isValid == True:
					# Set the text fields according to the XML file:
					self.percent_width.setText(result.xpath("/pnmconfig/geometry/width")[0].text.strip())
					self.percent_height.setText(result.xpath("/pnmconfig/geometry/height")[0].text.strip())
					self.animation_time.setText(result.xpath("/pnmconfig/animation/totaltime")[0].text.strip())
					self.time_quanta.setText(result.xpath("/pnmconfig/animation/timequanta")[0].text.strip())
					self.lifetime.setText(result.xpath("/pnmconfig/animation/windowlifetime")[0].text.strip())
					self.skin_path.setText(result.xpath("/pnmconfig/skinpath")[0].text.strip())
					self.manager_lifetime.setText(result.xpath("/pnmconfig/manager/lifetime")[0].text.strip())
					
					if result.xpath("/pnmconfig/direction")[0].attrib["choice"] == "down":
						self.stacking_down.toggle()
					else:
						self.stacking_up.toggle()
					
					if result.xpath("/pnmconfig/position")[0].attrib["choice"] == "manual":
						xc = result.xpath("/pnmconfig/position/xcoord")
						yc = result.xpath("/pnmconfig/position/ycoord")
						xt = "400"
						yt = "300"

						if xc.__len__() == 1 and yc.__len__() == 1:
							xt = xc[0].text.strip()
							yt = yc[0].text.strip()

						self.aux_frame_xcoord = int(xt)
						self.aux_frame_ycoord = int(yt)
						self.startx.setText(xt)
						self.starty.setText(yt)
						self.manual_position.setChecked(True)
					elif result.xpath("/pnmconfig/position")[0].attrib["choice"] == "upperRight":
						self.manual_position.setChecked(False)
						self.upper_right_radio.toggle()
					else:
						self.manual_position.setChecked(False)
						self.lower_right_radio.toggle()
					
					self.current_file = file_list[0]
					self.UpdateLooks()
				# If the file is not valid, show the error to the user:
				else:
					message_box = QtGui.QMessageBox(self)
					message_box.setWindowTitle(_("Error parsing configuration file"))
					message_box.setText(_("The configuration file %(config_file_name)s is not a valid configuration file.\nXSD Validation Error:\n%(error_string)s" % {"config_file_name" : self.current_file, "error_string" : result}))
					message_box.exec_()
					self.current_file = None
				return

			def closeEvent(self, close_event):
				self.Destroy()

			def Destroy(self):
				quit()

		return ConfigUI

# If executed as the main program:
if __name__ == "__main__":
	if sys.argv.__len__() != 2:
		print _("usage: %s <config_file>" % sys.argv[0])
		sys.exit(1)
	app = QtGui.QApplication(sys.argv)
	config_window = Configurator(sys.argv[1])
	config_window.Display()
	sys.exit(app.exec_())
else:
	print _("This program is not meant to be loaded as a module.")

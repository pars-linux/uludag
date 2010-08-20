#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# 
#
 
import sys
import os
import hashlib

from PyQt4 import QtCore, QtGui

from linuxtools import PartitionUtils

from functions import get_disk_info
from functions import get_iso_size
from functions import check_size

from ui_main import Ui_Dialog
from ui_selectdisk import Ui_SelectDialog
from ui_progressbar import Ui_ProgressDialog


class Start(QtGui.QMainWindow):
  	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)
       
	        #self.button_create_clicked = Create()

		self.connect(self.ui.button_cancel, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
    
		QtCore.QObject.connect(self.ui.button_open, QtCore.SIGNAL("clicked()"), self.open_file)
		QtCore.QObject.connect(self.ui.select_disk, QtCore.SIGNAL("clicked()"), self.select_disk)
                QtCore.QObject.connect(self.ui.button_create, QtCore.SIGNAL("clicked()"), self.button_create_clicked)
    
        @QtCore.pyqtSignature("bool")  
        def open_file(self):
                #select image file
		self.img_src = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select CD image"), os.environ["HOME"], "%s (*.iso *.img)" % self.tr("Images"))   
		
                #will be deleted
		self.ui.label.setText(self.img_src)
    
        @QtCore.pyqtSignature("bool")  
        def select_disk(self):
                # select portable disk
		self.sd = selectDisk()
      
		#linux tools
		self.a = PartitionUtils()
		self.a.detect_removable_drives()
	        
		#windows tools
		# self.a = ??
		  
		for key in  self.a.drives:
			self.sd.listWidget.insertItem(0,key)
	  		    
		self.connect(self.sd.listWidget, QtCore.SIGNAL("itemClicked(QListWidgetItem *)"), self.get_disk_destination)
		self.sd.exec_()
    
        @QtCore.pyqtSignature("bool")  
        def get_disk_destination(self, item):
		self.ui.label_2.setText(item.text())
		self.disk_dest = item.text()
	
		#will be deleted
		print self.a.drives[str(self.disk_dest)]
		self.ui.label_2.setText(str(self.a.drives[str(self.disk_dest)]['size']))
	
	@QtCore.pyqtSignature("bool")
	def button_create_clicked(self):
		self.img_size = get_iso_size(str(self.img_src))
		self.ui.label.setText(str(self.img_size))
		
		#self.a.mount_device(self.disk_dest)
		#self.a.unmount_device(str(self.disk_dest))

		if self.a.drives[str(self.disk_dest)]['is_mount'] == '1' :
			
			warningBox = QtGui.QMessageBox()
			warningBox.setText("Usb disk is mounted!")
			warningBox.setInformativeText("Please Unmount Disk!")
			warningBox.setWindowTitle("Warning!")
			warningBox.exec_()
				
		else:
			
			self.disk_size = int(self.a.drives[str(self.disk_dest)]['size'])
			
			if self.img_size > self.disk_size:
				req_size = self.img_size - self.disk_size
				msgBox = QtGu.QmessageBox()
				msgBox.setWindowTitle("Warning")
				msgBox.setText("There is no enough space!")
				msgBox.setInformativeText("%d more space required" % req_size)

			else:
				check_sum = ProgressCheckSum()
                                iso_file = open(self.img_src, "r")
                                iso_sha = hashlib.sha1()
                                iso_sha.update(iso_file.read())

                                shaBox = QtGui.QMessageBox()
                                shaBox.setText("Sha1sum of the iso:")
                                shaBox.setInformativeText("%s" % iso_sha.hexdigest())
                                shaBox.exec_()

				dest = open(self.disk_dest, 'w')
				by = 1024
				bytes = 0
			
				print self.disk_dest
			#	iso_file = open(self.img_src, "r")	
			#	while bytes <= ((self.img_size)*(1024**2)):
			#		data = iso_file.read(by)
			#		dest.write(data)
			#		bytes+=by
		
			#	copyInfo = QtGui.QMessageBox()
			#	copyInfo.setText("Copy Successed!")
			#	copyInfo.exec_()


class ProgressBar(QtGui.QDialog, Ui_ProgressDialog):
	def __init__(self, max_value, parent = None):
		super(ProgressBar, self).__init__(parent)
		self.setupUi(self)
		
		self.progressBar.setMaximum(max_value)
		
	def incrementProgress(self):
			 current_value = self.progressBar.value()
			 self.progressBar.setValue(current_value + 1)
	

#class ProgressCheckSum(QtCore.Qthread):
#	def __init_-(self, dialog, source)

class selectDisk(QtGui.QDialog, Ui_SelectDialog):  
      def __init__(self):
	      QtGui.QDialog.__init__(self)
	      self.setupUi(self)

        
if __name__ == "__main__":
    app= QtGui.QApplication(sys.argv)
    myapp = Start()
    myapp.show()
    sys.exit(app.exec_())

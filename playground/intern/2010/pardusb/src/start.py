#!/usr/bin/python
# -*- coding: utf-8 -*-
#

import sys
import hashlib
import os

if sys.platform == 'win32':
    platform = 'win32'
    from wintools import *
    
elif sys.platform == 'linux2':
    platform = 'linux2'
    from linuxtools import *

from PyQt4 import QtCore, QtGui

from ui_main import Ui_Dialog
import ui_selectdisk
import ui_progressbar
import ui_confirm

#from releases import *

mbyte = (1024**2)


class Start(QtGui.QMainWindow):
  	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_Dialog()
		self.ui.setupUi(self)

		self.connect(self.ui.button_cancel, QtCore.SIGNAL("clicked()"), QtCore.SLOT("close()"))
    
		QtCore.QObject.connect(self.ui.button_open, QtCore.SIGNAL("clicked()"), self.open_file)
		QtCore.QObject.connect(self.ui.select_disk, QtCore.SIGNAL("clicked()"), self.select_disk)
                QtCore.QObject.connect(self.ui.button_create, QtCore.SIGNAL("clicked()"), self.button_create_clicked)
	             
        @QtCore.pyqtSignature("bool")  
        def open_file(self):
                #select image file
            if platform == 'linux2':
                self.img_src = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select CD image"), os.environ["HOME"], "%s (*.iso *.img)" % self.tr("Images"))   
                
            elif platform == 'win32':
               self.img_src = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select CD image"))   # fix it 
            
                #will be deleted
            self.ui.lineEdit.setText(self.img_src)
    
        @QtCore.pyqtSignature("bool")  
        def select_disk(self):
                # select portable disk
		self.sd = selectDisk()
      		#linux tools
		if platform == 'linux2':
                    self.a = PartitionUtils()
                    self.a.detect_removable_drives()
                    
                    for key in  self.a.drives:
			self.sd.listWidget.insertItem(0,key)
	        
		#windows tools
                elif platform == 'win32':
                    self.a = win32_PartitionUtils()
                    self.a.win32_detect_removable_drives()

                    for key in self.a.drives:
                        self.sd.listWidget.insertItem(0,key)		
	  		    	    
		self.connect(self.sd.listWidget, QtCore.SIGNAL("itemClicked(QListWidgetItem *)"), self.get_disk_destination)
		self.sd.exec_()
		
    
        @QtCore.pyqtSignature("bool")  
        def get_disk_destination(self, item):		
		self.ui.lineEdit_2.setText(item.text())
		self.disk_dest = str(item.text())
		
		print self.a.drives[str(self.disk_dest)]
		  
                
	@QtCore.pyqtSignature("bool")
	def button_create_clicked(self):		  
		str(self.disk_dest)		
		self.img_size = os.stat(self.img_src).st_size / mbyte
		

		if platform == 'linux2':
                    self.disk_size = (int(self.a.drives[self.disk_dest]['size']) / mbyte)
                    
                    if self.a.drives[self.disk_dest]['is_mount'] == '1':
			  self.a.unmount_device(str(self.disk_dest)) # unmount!
			  print ("Disk is unmounted by HAL!")
                    
                    #self.a.mount_device(self.disk_dest) 

                elif platform == 'win32':
                    self.disk_size = self.a.win32_get_total_size()
                    print self.disk_size

		if self.a.drives[self.disk_dest]['is_mount'] == '1' :		
			self.warning_dialog(self.tr("Warning!"), self.tr("Flash disk is Mounted!\nPlease Unmount Disk")) 
	
		else:		  
			if self.img_size > self.disk_size:
				req_size = ((self.img_size - self.disk_size) / mbyte)

				self.warning_dialog(self.tr("Warning!"), self.tr("There is no enough space on drive!\n%dMB more space is required" % req_size ))
					
			else:	
                            	reply = QtGui.QMessageBox.question(self, self.tr('Sha1sum Check'), self.tr('Do you want to check integrity of image from sha1sum file?'), QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                                self.release = ''
                                if reply == QtGui.QMessageBox.Yes:
                                   self.release = self.__check_sum()
                                   
                                self.confirm_dialog =  confirmDialog(self.release, self.img_src, self.img_size, self.disk_size, self.disk_dest)
				
				if self.confirm_dialog.exec_() == QtGui.QDialog.Accepted: 
				    self.__burn_image()
				    				  
	def warning_dialog(self, title, text):
		QtGui.QMessageBox.warning(self, title, text, QtGui.QMessageBox.Ok)
			
	def __check_sum(self):
	  
            	sha_dest =  self.sha_dest = QtGui.QFileDialog.getOpenFileName(self, self.tr("Select Sha1sum File"), os.environ["HOME"], "%s (*.sha1sum)" % self.tr("Sha1sum"))   
                sha_file = open(sha_dest, 'rb')
                
                a =  sha_file.read()
                data = a.partition(' ')
                shasum = data[0]
                print data
                print "shasum from file: %s" % shasum
                print "Pardus release: %s" % data[2]
                release = data[2]
                           
		self.max_value = int(self.img_size)
		
		def close_dialog(): # wtf!
		  pb.close()
		  cs.quit()

		pb = progressBar(title = self.tr("Verify sha1sum"), message = self.tr("The integrity of image file is checking..."), max_value = self.max_value)                               			
                cs = checksumProgress(source = self.img_src)

                QtCore.QObject.connect(cs, QtCore.SIGNAL("incrementProgress()"), pb.incrementProgress)
		QtCore.QObject.connect(cs, QtCore.SIGNAL("closeProgress()"), close_dialog)

		cs.start()		
                pb.exec_()
		cs.wait()  
		
		
		if not cs.checksum():
		  print "Checksum cannot validated!"
		
                elif shasum == cs.checksum():
                    return release
                
                elif shasum != cs.checksum():
                    return "Sha1sum file is different than images shasum!"
		  

	def __burn_image(self):
	  
		def close_dialog(): # wtf!
		    copy_progress_bar.close()
		    copy_progress.quit()
		    
		copy_progress_bar = progressBar(title = self.tr("Copy Progress"), message = self.tr("Copy progress is running..."), max_value = int(self.img_size) )				    
		copy_progress = copyProgress(img_source = self.img_src, disk_dest = self.disk_dest, img_size = self.img_size) 
                                    
                QtCore.QObject.connect(copy_progress, QtCore.SIGNAL("copyIncrementProgress()"), copy_progress_bar.incrementProgress)
                QtCore.QObject.connect(copy_progress, QtCore.SIGNAL("closeProgress()"), close_dialog)
                                                   
                copy_progress.start()
                copy_progress_bar.exec_()
                copy_progress.wait()
                
		self.warning_dialog(self.tr("USB Image is Ready"), self.tr("USB image is ready. Hayrini Gor!"))

		return True	

class copyProgress(QtCore.QThread):
    def __init__(self, img_source, disk_dest, img_size):
    	QtCore.QThread.__init__(self)
        self.dest = open(disk_dest, "w")        
        self.src = open(img_source, "r")
        self.img_size = (img_size * mbyte)

    def run(self):       
        by = mbyte
        bytes = 0 
        
        print "Copy progress is started!"
        
        while bytes <= self.img_size:
            data = self.src.read(by)
            self.dest.write(data)
            bytes += by
            self.emit(QtCore.SIGNAL("copyIncrementProgress()"))

        print "Copy progress is finished!"
        self.emit(QtCore.SIGNAL("closeProgress()"))
        print "CloseProgress() signal is send!!"
        
class checksumProgress(QtCore.QThread):
	def __init__(self, source):
	      QtCore.QThread.__init__(self)
	      self.src = source
	      self.cnt = 0
	      
	def run(self): 
            iso = open(self.src, "rb")
	  
            bytes = mbyte
            sha = hashlib.sha1()
	    print "Checksum progress is started!"
	    
            while bytes:
		data = iso.read(bytes)
		sha.update(data)
		bytes = len(data)
		self.emit(QtCore.SIGNAL("incrementProgress()"))
		
            self.shasum = sha.hexdigest()
            print "Checksum progress is finished!"
            self.emit(QtCore.SIGNAL("closeProgress()"))
	
	def checksum(self): # return release name etc if exist!
	    print "Sha1sum of the iso: %s" % self.shasum
            return self.shasum
	  
class progressBar(QtGui.QDialog, ui_progressbar.Ui_Dialog):
	def __init__(self, title, message, max_value, parent = None):
		super(progressBar, self).__init__(parent)
		self.setupUi(self)
		self.progressBar.setMinimum(0)
		self.label.setText(message)
		self.setWindowTitle(title)
		self.progressBar.setValue(0)
		self.progressBar.setMaximum(max_value)
		#print max_value
	
	@QtCore.pyqtSignature("bool")
	def incrementProgress(self):
			 #print "incrementing value.."
			 current_value = self.progressBar.value()
			 self.progressBar.setValue(current_value + 1)
	
	@QtCore.pyqtSignature("bool")
	def close_progress(self):
	      print ("close progressbar!!")
	      self.progressBar.close()
	
class selectDisk(QtGui.QDialog, ui_selectdisk.Ui_Dialog):  
      def __init__(self):
	      QtGui.QDialog.__init__(self)
	      self.setupUi(self)

class confirmDialog(QtGui.QDialog, ui_confirm.Ui_Dialog):
      def __init__(self, sha_sum, img_src, img_size, disk_size, disk_dest):
	      QtGui.QDialog.__init__(self)
	      self.setupUi(self)
	      
	      self.label_img_path.setText(img_src)
	      self.label_img_size.setText("%dMB" % img_size)
	      self.label_release.setText(sha_sum)
	      self.label_dest_size.setText("%dMB" % disk_size)
	      self.label_disk_path.setText(disk_dest)
	     
if __name__ == "__main__":
    app= QtGui.QApplication(sys.argv)
    myapp = Start()
    myapp.show()
    sys.exit(app.exec_())

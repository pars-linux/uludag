#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Alper Tokgöz
#


import os



def get_disk_info(disk_dest):

	disk_info = os.statvfs(disk_dest)
        capacity = int(disk_info.f_bsize *disk_info.f_blocks / 1024**2)
        available = int(disk_info.f_bsize * disk_info.f_bavail / 1024**2)
        used = int(disk_info.f_bsize * (disk_info.f_blocks - disk_info.f_bavail) / 1024**2)
  
  
        return [capacity, available, used]
  
def get_iso_size(img_src):
  	return os.stat(img_src).st_size / 1024**2
  
  

def check_size(img_size, avail_disk_size):
	if  img_size > avail_disk_size:
		req_size = img_size - avail_disk_size
		msgBox = QMessageBox()
		msgBox.setText("There is no enough space!")
		msgBox.setInformativeText(" %s more space required" % req_size)
		return 0
		msbBox.exec_()


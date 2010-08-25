# -*- coding: utf-8 -*-

import win32file, win32api
import os

class win32_PartitionUtils:
    def __init__(self):
        self.drives = {}
        
    def win32_get_total_size(drive=None):
        r = win32file.GetDiskFreeSpace('C:')
        capacity = r[3]*r[0]*r[1] / (1024**2)    #capacity = totalClusters*sectPerCluster*bytesPerSector as MegaByte
        return capacity

    def win32_detect_removable_drives(self):
        for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            try:
                drive = drive + ':'
                if win32file.GetDriveType(drive) != win32file.DRIVE_REMOVABLE: #will be changed                    
                        r = win32file.GetDiskFreeSpace(drive)
                        capacity = r[3]*r[0]*r[1] / (1024**2)    #capacity = totalClusters*sectPerCluster*bytesPerSector as MegaByte
                        print capacity
                        print r
                        
                        self.drives[drive] = { 
                          'label': 'label', 
                          'mount': drive, 
                          'size': capacity,  
                          'device': drive,
                          'is_mount' : 1 # will be edited
                      } 
            except:
                pass

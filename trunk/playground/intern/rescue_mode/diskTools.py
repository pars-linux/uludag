# -*- coding: utf-8 -*-
import glob
import os
from pardus import diskutils
import comar
import parted
import subprocess

def getPartitionsLabels():
  
  partitionsLabels=[]
  
  for i in glob.glob("/dev/disk/by-label/*"):
    partitionsLabels.append(i.lstrip("/dev/disk/by-label/"))
  
  return partitionsLabels
  
def getPardusPartitions():
  
  pardusPartitions = []
  
  for i in getPartitionsLabels():
    if "PARDUS_ROOT" in i:
	i = [i,diskutils.getDeviceByLabel(i)]
	pardusPartitions.append(i)
	
  return pardusPartitions



def getWinBootPartitions():

  winBootPartitions = []
  deviceList = diskutils.getDeviceMap()

  for i in deviceList:
    device = parted.PedDevice.get(i[1])
    disk = parted.PedDisk.new(device)
    path = disk.next_partition()
    while path:
      if path.num >= 1:
	if path.fs_type.name in ("ntfs", "fat32"):
	  if isWindowsBoot("%s%d"%(i[1],path.num),path.fs_type.name):
	    winBootPartitions.append([i[1],path.num,path.fs_type.name,"%s%d"%(i[1],path.num)])
      path = disk.next_partition(path)

  return winBootPartitions

def isWindowsBoot(partition_path, file_system):
    m_dir = "/tmp/_pcheck"
    if not os.path.isdir(m_dir):
        os.makedirs(m_dir)
    umount(m_dir)
    try:
        if file_system == "fat32":
            mount(partition_path, m_dir, "vfat")
        else:
            mount(partition_path, m_dir, file_system)
    except:
        return False

    exist = lambda f: os.path.exists(os.path.join(m_dir, f))

    if exist("boot.ini") or exist("command.com") or exist("bootmgr"):
        umount(m_dir)
        return True
    else:
        umount(m_dir)
        return False
        
def mount(source, target, fs):
    subprocess.call("mount -t %s %s %s"%(fs,source,target),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
def umount(target):
    subprocess.call("umount %s"%(target),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  
        
def getPardusPartInfo():
  
  pardusPartInfo = []
  link = comar.Link()
  for i in getPardusPartitions():
    path = "/mnt/rescue_disk/"+i[0]
    if os.path.exists(path):
      mounteds= link.Disk.Manager["mudur"].getMounted()
      if path in str(mounteds):
	#comar.Link().Disk.Manager["mudur"].umount(path)
	pass
    else:
      os.makedirs(path)
    comar.Link().Disk.Manager["mudur"].mount(i[1],path)
    pardusPartInfo.append([open(path+"/etc/pardus-release").read().rstrip("\n"),i[1],i[0],path])
  
  pardusPartInfo.reverse()
  
  return pardusPartInfo

def get_partitions_path(disk):
    link = comar.Link()
    mounteds = link.Disk.Manager["mudur"].getMounted()
    return str(filter(lambda part: part[0]==disk,mounteds)[0][1])
  
def main():
  print detectAll("/dev/sda")
  

if __name__=="__main__":
  main()
    

  
  

  

# -*- coding: utf-8 -*-
import glob
import os
from pardus import diskutils
import comar
import parted
from shellTools import run_quiet


def getDeviceModel(devices):
  devices_model = []
  for i in devices:
    deviceName = parted.PedDevice.get(i[1]).model
    devices_model.append([deviceName,i])
  return devices_model
    
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
        
def getPardusPartInfo():
  
  pardusPartInfo = []
  link = comar.Link(socket="/var/run/dbus/system_bus_socket")
  for i in getPardusPartitions():
    path = "/mnt/rescue_disk/"+i[0]
    if os.path.exists(path):
      flag = True
      for mounted in link.Disk.Manager["mudur"].getMounted():
	if str(mounted[1])==path:
	  flag = False
	  if str(mounted[0])!=i[1] :
	    link.Disk.Manager["mudur"].umount(path)
	    link.Disk.Manager["mudur"].mount(i[1],path)
      if flag:
	link.Disk.Manager["mudur"].mount(i[1],path)
    else:
      os.makedirs(path)
      link.Disk.Manager["mudur"].mount(i[1],path)
    pardusPartInfo.append([open(path+"/etc/pardus-release").read().rstrip("\n"),i[1],i[0],path])

  
  return pardusPartInfo


def getWindowsPartitions():

  windowsPartitions = []
  deviceList = diskutils.getDeviceMap()

  for i in deviceList:
    device = parted.PedDevice.get(i[1])
    disk = parted.PedDisk.new(device)
    path = disk.next_partition()
    while path:
      if path.fs_type:
	if path.fs_type.name in ("ntfs", "fat32"):
	  if isWindowsBoot("%s%d"%(i[1],path.num),path.fs_type.name):
	    windowsPartitions.append([i[1],path.num,path.fs_type.name,"%s%d"%(i[1],path.num)])
      path = disk.next_partition(path)

  return windowsPartitions

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
    run_quiet("mount -t %s %s %s"%(fs,source,target))
def umount(target):
    run_quiet("umount %s"%(target))
  



def main():
  print detectAll("/dev/sda")
  

if __name__=="__main__":
  main()
    

  
  

  

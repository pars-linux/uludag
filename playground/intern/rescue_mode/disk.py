# -*- coding: utf-8 -*-
import glob
import os
from pardus import diskutils
import comar

def getPartitionsLabels():
  
  partitionsLabels=[]
  
  for i in glob.glob("/dev/disk/by-label/*"):
    partitionsLabels.append(i.lstrip("/dev/disk/by-label/"))
  
  return partitionsLabels
  
def getPardusPartitions():
  
  pardusPartitions=[]
  
  for i in getPartitionsLabels():
    if "PARDUS_ROOT" in i:
	i = [i,diskutils.getDeviceByLabel(i)]
	pardusPartitions.append(i)
	
  return pardusPartitions
  
def getPardusVLP():
  
  pardusVLP = []
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
    #comar.Link().Disk.Manager["mudur"].mount(i[1],path)
    pardusVLP.append([open(path+"/etc/pardus-release").read().rstrip("\n"),i[1],i[0],path])
  
  pardusVLP.reverse()
  
  return pardusVLP

def get_partitions_path(disk):
    link = comar.Link()
    mounteds = link.Disk.Manager["mudur"].getMounted()
    return str(filter(lambda part: part[0]==disk,mounteds)[0][1])
  
def main():
  pass
  
if __name__=="__main__":
  main()
    

  
  

  

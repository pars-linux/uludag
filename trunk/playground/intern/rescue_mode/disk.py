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
    if "PARDUS_ROOTx" in i:
	i = [i,diskutils.getDeviceByLabel(i)]
	pardusPartitions.append(i)
	
  return pardusPartitions
  
def getPardusVLP():
  
  pardusVLP = []
  
  for i in getPardusPartitions():
    path = "/mnt/rescue_disk/"+i[0]
    if os.path.exists(path):
     # pass
      comar.Link().Disk.Manager["mudur"].umount(path)
    else:
      os.makedirs(path)
    comar.Link().Disk.Manager["mudur"].mount(i[1],path)
    pardusVLP.append([open(path+"/etc/pardus-release").read().rstrip("\n"),i[0],i[1]])
  
  pardusVLP.reverse()
  
  return pardusVLP


  
def main():
  pass
  
if __name__=="__main__":
  main()
    

  
  

  

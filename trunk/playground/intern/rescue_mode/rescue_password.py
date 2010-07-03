# -*- coding: utf-8 -*-
import os, dbus, comar, subprocess


_sys_dirs = ["dev","proc","sys"]

def chrootRun(path,cmd):
    temp = "chroot %s %s" % (path, cmd)
   # print temp
   # os.system(temp)
    subprocess.call(temp,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class pardusDbus:
  def __init__(self,path):
      
    for _dir in _sys_dirs:
        tgt = os.path.join(path, _dir)
	temp = "mount --bind /%s %s" % (_dir, tgt)
	#print temp
        os.system(temp)
  
     
    chrootRun(path,"/sbin/ldconfig")
    chrootRun(path,"/sbin/update-environment")
    chrootRun(path,"/bin/service dbus start")
    
    self.sokcet_file = os.path.join(path,"var/run/dbus/system_bus_socket")
    #print self.sokcet_file
    asd = "unix:path=%s" %self.sokcet_file
    #print asd
    dbus.bus.BusConnection(address_or_type=asd)
    
  def getUserlist(self):
      link = comar.Link(socket=self.sokcet_file)
      users = link.User.Manager["baselayout"].userList()
      return filter(lambda user: user[0]==0 or (user[0]>=1000 and user[0]<=65000), users)

def main():
  a = pardusDbus("/mnt/rescue_disk/PARDUS_ROOT")
  print a.getUserlist()

if __name__ == "__main__":
  main()
    

  
  
 

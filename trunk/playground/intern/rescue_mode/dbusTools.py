# -*- coding: utf-8 -*-
import os, dbus, comar, subprocess


_sys_dirs = ["dev","proc","sys"]

def chrootRun(path,cmd):
    subprocess.call("chroot %s %s" % (path, cmd),shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)


class pardusDbus:
  def __init__(self,path):
      
    for _dir in _sys_dirs:
        tgt = os.path.join(path, _dir)
        os.system("mount --bind /%s %s" % (_dir, tgt))
       
    chrootRun(path,"/sbin/ldconfig")
    chrootRun(path,"/sbin/update-environment")
    chrootRun(path,"/bin/service dbus start")
    
    self.sokcet_file = os.path.join(path,"var/run/dbus/system_bus_socket")
     
    dbus.bus.BusConnection(address_or_type="unix:path=%s" %self.sokcet_file)
    link = comar.Link(socket=self.sokcet_file)
    self.baselayout = link.User.Manager["baselayout"]
  def getUserlist(self):
 
    users = self.baselayout.userList()
    return filter(lambda user: user[0]==0 or (user[0]>=1000 and user[0]<=65000), users)
  
  def setUserPass(self,uid, password):
    info = self.baselayout.userInfo(uid)
    return self.baselayout.setUser(uid, info[1], info[3], info[4], password, info[5])

def main():
  a = pardusDbus("/mnt/rescue_disk/PARDUS_ROOT")
  print a.getUserlist()

if __name__ == "__main__":
  main()
    

  
  
 

# -*- coding: utf-8 -*-
import os, dbus, comar, subprocess, pisi
from shellTools import chrootRun


_sys_dirs = ["dev","proc","sys"]



class pardusDbus:
  def __init__(self,path):
    self.path = path 
    for _dir in _sys_dirs:
        tgt = os.path.join(path, _dir)
        os.system("mount --bind /%s %s" % (_dir, tgt))
       
    chrootRun(path,"/sbin/ldconfig")
    chrootRun(path,"/sbin/update-environment")
    chrootRun(path,"/bin/service dbus start")
    
    self.socket_file = os.path.join(path,"var/run/dbus/system_bus_socket")
     
    dbus.bus.BusConnection(address_or_type="unix:path=%s" %self.socket_file)
    link = comar.Link(socket=self.socket_file)
    self.baselayout = link.User.Manager["baselayout"]
    
    options = pisi.config.Options()
    options.yes_all = True
    options.ignore_dependency = True
    options.ignore_safety = True
    options.destdir=path
    
 #   dbus.SystemBus()
    
    pisi.api.set_dbus_sockname(self.socket_file)
    pisi.api.set_dbus_timeout(1200)
    pisi.api.set_options(options)
    pisi.api.set_comar(True)
    pisi.api.set_signal_handling(False)
    
  def getUserlist(self):
 
    users = self.baselayout.userList()
    return filter(lambda user: user[0]==0 or (user[0]>=1000 and user[0]<=65000), users)
  
  def setUserPass(self,uid, password):
    info = self.baselayout.userInfo(uid)
    return self.baselayout.setUser(uid, info[1], info[3], info[4], password, info[5])

  def getHistory(limit=50):
    pdb = pisi.db.historydb.HistoryDB()
    result = []
    i=0
    for op in pdb.get_last():
        # Dont add repo updates to history list
        if not op.type == 'repoupdate':
            result.append(op)
            i+=1
            if i==limit:
                break
    return result
  
  def takeBack(self,operation):
    # dirty hack for COMAR to find scripts.
    os.symlink("/",self.path + self.path)
    pisi.api.takeback(operation)
    os.unlink(self.path +self.path)

    
  


def main():
  a = pardusDbus("/mnt/rescue_disk/PARDUS_ROOT")
  for b in a.getHistory():
    print b.no
  
  print ""
 # a = pardusDbus("/mnt/rescue_disk/PARDUS_ROOT1")
  #for b in a.getHistory():
   # print b.no
  

if __name__ == "__main__":
  main()
    

  
  
 

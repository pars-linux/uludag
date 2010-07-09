# -*- coding: utf-8 -*-
import os, dbus, comar, subprocess, pisi
import shellTools
import time

_sys_dirs = ["dev","proc","sys"]



class pardusDbus:
  def __init__(self,path):
    self.path = path 
    for _dir in _sys_dirs:
        tgt = os.path.join(path, _dir)
        shellTools.mount(_dir, tgt,param="--bind")
       
    shellTools.chrootRun(path,"/sbin/ldconfig")
    shellTools.chrootRun(path,"/sbin/update-environment")
    shellTools.chrootRun(path,"/bin/service dbus start")
    
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
    try:
	info = self.baselayout.userInfo(uid)
	if self.baselayout.setUser(uid, info[1], info[3], info[4], password, info[5]):
	  return ["message","değişmedi"]
	else:
	  return ["message","değişti"]
    except dbus.DBusException as error:
	return ["error",error.message]

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
    #for i in result:
    #  print "%d"%i.no
     # print "---"
    #time.sleep(5)
    return result
  
  def takeBack(self,operation):
    # dirty hack for COMAR to find scripts.
    os.symlink("/",self.path + self.path)
    pisi.api.takeback(operation)
    os.unlink(self.path +self.path)
    
  def finalizeChroot(self):
    # close filesDB if it is still open
    historydb = pisi.db.historydb.HistoryDB()
    if historydb.is_initialized():
	#print "merhaba"
	time.sleep(5)
        historydb.cache_flush()

    # stop dbus
    shellTools.chrootRun(self.path,"/bin/service dbus stop")

    # kill comar in chroot if any exists
    shellTools.chrootRun(self.path,"/bin/killall comar")

    # unmount sys dirs
    c = _sys_dirs
    c.reverse()
    for _dir in c:
        tgt = os.path.join(self.path, _dir)
        shellTools.umount(tgt)

    # swap off if it is opened
    shellTools.run_quiet("swapoff -a")

    # umount target dir
 #   umount_(self.path)
    
  


#def main():
  
  

if __name__ == "__main__":
  pass
 # main()
    

  
  
 

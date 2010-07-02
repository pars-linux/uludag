# -*- coding: utf-8 -*-
import os, dbus, comar


_sys_dirs ["dev","proc","sys"]

def chrootRun(cmd):
    os.system("chroot %s %s" % ("/", cmd))


class pardus_dbus:
  def __init__(self,path):
    for _dir in _sys_dirs:
        tgt = os.path.join(path, _dir)
        os.system("mount --bind /%s %s" % (_dir, tgt))

    chrootRun("/sbin/ldconfig")
    chrootRun("/sbin/update-environment")
    chrootRun("/bin/service dbus start")
    
    sokcet_file = os.path.join(path,"var/run/dbus/system_bus_socket")
    dbus.bus.BusConnection(address_or_type="unix:path=%s" % sokcet_file)
    
def get_userlist():
    link = comar.Link(socket=ctx.consts.dbus_socket_file)
    users = link.User.Manager["baselayout"].userList()
    return filter(lambda user: user[0]==0 or (user[0]>=1000 and user[0]<=65000), users)
    

  
  
 

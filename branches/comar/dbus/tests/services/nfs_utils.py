import os
import signal
from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "NFS Daemon",
                 "tr": "NFS Sunucusu"})

def start():
    startDependencies("portmap")
    startService("/usr/sbin/rpc.idmapd")
    startService("/sbin/rpc.statd")
    startService("/usr/sbin/exportfs", args="-r")
    startService("/usr/sbin/rpc.nfsd")
    startService("/usr/sbin/rpc.mountd", donotify=True)

def stop():
    stopService(command="/usr/sbin/rpc.mountd")
    stopService(name="nfsd", user="root", signal=signal.SIGINT)
    stopService(command="/usr/sbin/exportfs", args="-ua")
    stopService(command="/sbin/rpc.statd")
    stopService(command="/usr/sbin/rpc.idmapd", donotify=True)

def status():
    return isServiceRunning("/var/run/rpc.statd.pid")

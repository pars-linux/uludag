from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "vsFTP Daemon",
                 "tr": "vsFTP Sunucusu"})

@synchronized
def start():
    if 0 != run("/sbin/modprobe capability"):
        fail("cannot load capability module")
    startService(command="/usr/sbin/vsftpd",
                 args="/etc/vsftpd/vsftpd.conf",
                 pidfile="/var/run/vsftpd.pid",
                 makepid=True,
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/vsftpd.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/vsftpd.pid")

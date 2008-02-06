from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "TFTP Daemon",
                 "tr": "TFTP Sunucusu"})

@synchronized
def start():
    startService(command="/usr/sbin/in.tftpd",
                 args="-s -l /tftpboot",
                 donotify=True)

@synchronized
def stop():
    stopService(command="/usr/sbin/in.tftpd",
                donotify=True)

def status():
    return isServiceRunning(command="/usr/sbin/in.tftpd")

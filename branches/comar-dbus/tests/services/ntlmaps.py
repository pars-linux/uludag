from pardus.serviceutils import *

serviceType = "local"
serviceDesc = _({"en": "NTLM Proxy Daemon",
                 "tr": "NTLM Vekil Sunucusu"})

@synchronized
def start():
    startService(command="/usr/bin/python",
                 args="/usr/bin/ntlmaps",
                 pidfile="/var/run/ntlmaps.pid",
                 makepid=True,
                 chuid="ntlmaps",
                 detach=True,
                 donotify=True)

@synchronized
def stop():
    stopService(pidfile="/var/run/ntlmaps.pid",
                donotify=True)

def status():
    return isServiceRunning("/var/run/ntlmaps.pid")

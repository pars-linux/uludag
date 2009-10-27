from pardus.serviceutils import *

serviceType = "server"
serviceDesc = _({"en": "AUDIT Daemon",
                 "tr": "AUDIT Sunucusu"})

@synchronized
def start():
    reply = startService(command="/sbin/auditd",
                         pidfile="/var/run/auditd.pid",
                         donotify=True)
    if reply == 0:
        run("/sbin/auditctl -R /etc/audit/audit.rules")

@synchronized
def stop():
    reply = stopService(pidfile="/var/run/auditd.pid",
                        donotify=True)
    if reply == 0:
        run("/sbin/auditctl -D")

def status():
    return isServiceRunning("/var/run/auditd.pid")
